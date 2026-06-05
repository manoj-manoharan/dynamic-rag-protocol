#!/usr/bin/env python3
"""Phase 3: Model Capability Profile - Test Harness"""

import argparse
import asyncio
import json
import logging
import os
import re
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generators import TESTS

# ═══════════════════════════════════════════════════════════════
# OLLAMA CLIENT
# ═══════════════════════════════════════════════════════════════

_executor = None


def _ollama_sync(model, prompt, system, base_url, timeout):
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        f"{base_url}/api/chat", data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    return {
        "text": data.get("message", {}).get("content", ""),
        "tokens_in": data.get("prompt_eval_count", 0),
        "tokens_out": data.get("eval_count", 0),
    }


async def call_ollama(model, prompt, system, base_url, timeout=120, retries=3):
    loop = asyncio.get_event_loop()
    for attempt in range(retries):
        try:
            return await loop.run_in_executor(
                _executor, _ollama_sync, model, prompt, system, base_url, timeout,
            )
        except Exception as e:
            if attempt < retries - 1:
                wait = 2 ** attempt
                logging.warning(f"Ollama error (attempt {attempt + 1}/{retries}): {e}. Retry in {wait}s")
                await asyncio.sleep(wait)
            else:
                raise


# ═══════════════════════════════════════════════════════════════
# PROMPT FORMATTING
# ═══════════════════════════════════════════════════════════════

def format_prompt(inputs):
    """Build (prompt, system) from generator inputs. Shape determines type."""
    if "facts" in inputs:
        context = "\n".join(inputs["facts"])
        prompt = (
            f"Based ONLY on the following information, answer the question precisely.\n\n"
            f"INFORMATION:\n{context}\n\n"
            f"QUESTION: {inputs['question']}\n\n"
            f"Respond in this exact format:\n"
            f"ANSWER: [your answer]\n"
            f"If you cannot determine the answer, respond:\n"
            f"UNCERTAIN: [reason]"
        )
        return prompt, "Answer precisely based only on provided information. Use the exact format requested."

    if "sentence" in inputs:
        entity_list = ", ".join(inputs["entities"])
        prompt = (
            f"Given this sentence and list of known entities, identify which entities "
            f"from the list appear or are referenced in the sentence.\n\n"
            f"SENTENCE: {inputs['sentence']}\n\n"
            f"KNOWN ENTITIES: {entity_list}\n\n"
            f"Respond in this exact format:\n"
            f"FOUND: [comma-separated entities from the list, or NONE]\n"
            f"NEW: [comma-separated new entities not in the list, or NONE]"
        )
        return prompt, "Extract structured information precisely. Use the exact format requested."

    raise ValueError(f"Unknown input shape: {list(inputs.keys())}")


# ═══════════════════════════════════════════════════════════════
# CHECKERS
# ═══════════════════════════════════════════════════════════════

def judge(response, expected, config):
    """Returns (judgment, format_compliant). Judgment is one of:
    correct, abstained, confident_wrong, format_error."""
    if not response or not response.strip():
        return "format_error", False

    check_type = config["type"]

    # Reader checks (regex, regex_all)
    if check_type in ("regex", "regex_all"):
        if re.search(r"UNCERTAIN\s*:", response, re.IGNORECASE):
            return "abstained", True
        answer_m = re.search(r"ANSWER\s*:\s*(.*)", response, re.IGNORECASE | re.DOTALL)
        text = answer_m.group(1).strip() if answer_m else response
        fmt = bool(answer_m)
        if check_type == "regex":
            ok = bool(re.search(config["pattern"], text, re.IGNORECASE))
        else:
            ok = all(re.search(p, text, re.IGNORECASE) for p in config["patterns"])
        return ("correct" if ok else "confident_wrong"), fmt

    # Ingester check (entity_match)
    if check_type == "entity_match":
        found_m = re.search(r"FOUND\s*:\s*(.*?)(?:\n|$)", response, re.IGNORECASE)
        if not found_m:
            # Fallback: check whole response for expected entities
            ok = all(re.search(re.escape(e), response, re.IGNORECASE) for e in config["expected_found"])
            return ("correct" if ok else "format_error"), False
        found_text = found_m.group(1).strip()
        if found_text.upper() == "NONE":
            actual = []
        else:
            actual = [e.strip().lower() for e in found_text.split(",") if e.strip()]
        expected_lower = [e.lower() for e in config["expected_found"]]
        ok = all(any(exp in act for act in actual) for exp in expected_lower)
        return ("correct" if ok else "confident_wrong"), True

    raise ValueError(f"Unknown checker: {check_type}")


# ═══════════════════════════════════════════════════════════════
# RESULT STORE
# ═══════════════════════════════════════════════════════════════

class Store:
    def __init__(self, model, base="results"):
        self.model_slug = model.replace(":", "_").replace("/", "_")
        self.base = os.path.join(base, self.model_slug)

    def _dir(self, test, diff, ver):
        return os.path.join(self.base, test, diff, f"v{ver}")

    def latest_version(self, test, diff):
        d = os.path.join(self.base, test, diff)
        if not os.path.isdir(d):
            return 0
        vs = [int(x[1:]) for x in os.listdir(d) if x.startswith("v") and x[1:].isdigit()]
        return max(vs) if vs else 0

    def ensure_version(self, test, diff, force_new=False, reason=""):
        v = self.latest_version(test, diff)
        if v > 0 and not force_new:
            return v
        v += 1
        d = self._dir(test, diff, v)
        os.makedirs(d, exist_ok=True)
        meta = {
            "version": v, "model": self.model_slug,
            "created": datetime.now(timezone.utc).isoformat(),
            "reason": reason or ("new" if force_new else "initial"),
        }
        with open(os.path.join(d, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)
        return v

    def completed(self, test, diff, ver):
        path = os.path.join(self._dir(test, diff, ver), "trials.jsonl")
        if not os.path.exists(path):
            return set()
        done = set()
        with open(path) as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    done.add(json.loads(line)["trial"])
                except (json.JSONDecodeError, KeyError):
                    pass
        return done

    def write(self, test, diff, ver, result):
        d = self._dir(test, diff, ver)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "trials.jsonl"), "a") as f:
            f.write(json.dumps(result) + "\n")

    def find_failed_cells(self):
        """Return (test, diff) pairs where latest version has confident_wrong."""
        cells = []
        if not os.path.isdir(self.base):
            return cells
        for test in os.listdir(self.base):
            test_dir = os.path.join(self.base, test)
            if not os.path.isdir(test_dir):
                continue
            for diff in os.listdir(test_dir):
                if not os.path.isdir(os.path.join(test_dir, diff)):
                    continue
                v = self.latest_version(test, diff)
                if v == 0:
                    continue
                path = os.path.join(self._dir(test, diff, v), "trials.jsonl")
                if not os.path.exists(path):
                    continue
                with open(path) as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            if json.loads(line).get("judgment") == "confident_wrong":
                                cells.append((test, diff))
                                break
                        except json.JSONDecodeError:
                            pass
        return cells


# ═══════════════════════════════════════════════════════════════
# SEED
# ═══════════════════════════════════════════════════════════════

def compute_seed(test_name, difficulty, trial):
    """Deterministic seed from test coordinates."""
    h = 2166136261
    for c in f"{test_name}_{difficulty}":
        h = ((h ^ ord(c)) * 16777619) & 0xFFFFFFFF
    return (h + trial) & 0xFFFFFFFF


# ═══════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════

async def run_all(args):
    global _executor
    _executor = ThreadPoolExecutor(max_workers=args.concurrency)
    store = Store(args.model)
    sem = asyncio.Semaphore(args.concurrency)

    # Resolve test set
    tests = TESTS
    if args.tests:
        names = [t.strip() for t in args.tests.split(",")]
        unknown = [n for n in names if n not in TESTS]
        if unknown:
            logging.error(f"Unknown tests: {unknown}. Available: {list(TESTS.keys())}")
            sys.exit(1)
        tests = {k: v for k, v in TESTS.items() if k in names}

    # Handle --retry-failed: create new versions for cells with failures
    if args.retry_failed:
        cells = [(t, d) for t, d in store.find_failed_cells() if t in tests]
        if not cells:
            print("No failed cells found.")
            return
        print(f"Retrying {len(cells)} cells with failures...")
        for test, diff in cells:
            store.ensure_version(test, diff, force_new=True, reason="retry failed")

    # Build task list
    task_args = []
    for name, test in tests.items():
        diffs = test["difficulties"]
        if args.difficulty:
            diffs = [d for d in diffs if d == args.difficulty]
        for diff in diffs:
            ver = store.ensure_version(name, diff, force_new=args.new_version)
            done = store.completed(name, diff, ver)
            for t in range(test["trials"]):
                if t not in done:
                    task_args.append((name, test, diff, ver, t, compute_seed(name, diff, t)))

    if not task_args:
        print("All trials complete.")
        _executor.shutdown(wait=False)
        return

    progress = {"done": 0, "total": len(task_args), "start": time.monotonic()}
    marks = {"correct": "✓", "abstained": "?", "confident_wrong": "✗", "format_error": "!"}
    print(f"Running {len(task_args)} trials ({args.concurrency}x concurrency)...\n")

    async def run_one(name, test, diff, ver, trial_num, seed):
        async with sem:
            case = test["generator"](diff, trial_num, seed)
            prompt, system = format_prompt(case["inputs"])
            t0 = time.monotonic()
            try:
                resp = await call_ollama(args.model, prompt, system, args.ollama_url)
            except Exception as e:
                logging.error(f"SKIP {name}/{diff}/t{trial_num}: {e}")
                progress["done"] += 1
                return
            ms = int((time.monotonic() - t0) * 1000)
            judgment, fmt = judge(resp["text"], case["expected"], case["check"])
            result = {
                "trial": trial_num, "seed": seed, "judgment": judgment,
                "format_compliant": fmt, "expected": case["expected"],
                "response": resp["text"],
                "tokens_in": resp["tokens_in"], "tokens_out": resp["tokens_out"],
                "latency_ms": ms, "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            store.write(name, diff, ver, result)
            progress["done"] += 1
            elapsed = time.monotonic() - progress["start"]
            rate = progress["done"] / elapsed if elapsed > 0 else 1
            eta = int((progress["total"] - progress["done"]) / rate) if rate > 0 else 0
            logging.info(
                f'[{progress["done"]}/{progress["total"]}] '
                f'{name}/{diff}/t{trial_num} {marks[judgment]} {judgment} '
                f'({ms}ms) ETA:{eta}s'
            )

    await asyncio.gather(*[run_one(*t) for t in task_args])
    elapsed = time.monotonic() - progress["start"]
    print(f"\nDone. {progress['done']} trials in {elapsed:.0f}s")
    _executor.shutdown(wait=False)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def check_ollama(model, url):
    try:
        req = urllib.request.Request(f"{url}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            models = [m["name"] for m in json.loads(resp.read().decode()).get("models", [])]
        if not any(model in m for m in models):
            print(f"Model '{model}' not found. Available: {', '.join(models)}")
            print(f"Pull it: ollama pull {model}")
            sys.exit(1)
    except Exception as e:
        print(f"Cannot connect to Ollama at {url}: {e}")
        print("Start it: ollama serve")
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Phase 3: Model Capability Profile")
    p.add_argument("--model", default="gemma2:2b")
    p.add_argument("--tests", help="Comma-separated test names")
    p.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    p.add_argument("--concurrency", type=int, default=1)
    p.add_argument("--new-version", action="store_true")
    p.add_argument("--retry-failed", action="store_true")
    p.add_argument("--ollama-url", default="http://localhost:11434")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    os.makedirs("logs", exist_ok=True)
    log_file = os.path.join("logs", f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )

    print(f"Phase 3: Model Capability Profile")
    print(f"Model: {args.model} | Log: {log_file}")
    print(f"Available tests: {', '.join(TESTS.keys())}\n")

    check_ollama(args.model, args.ollama_url)
    asyncio.run(run_all(args))


if __name__ == "__main__":
    main()
