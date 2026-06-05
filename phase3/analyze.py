#!/usr/bin/env python3
"""Phase 3: Analyze test results."""

import argparse
import json
import os
import sys


def load_results(model_dir):
    """Load all results for a model. Returns {test: {diff: {ver: [trials]}}}."""
    results = {}
    if not os.path.isdir(model_dir):
        return results
    for test in sorted(os.listdir(model_dir)):
        test_dir = os.path.join(model_dir, test)
        if not os.path.isdir(test_dir):
            continue
        results[test] = {}
        for diff in os.listdir(test_dir):
            diff_dir = os.path.join(test_dir, diff)
            if not os.path.isdir(diff_dir):
                continue
            results[test][diff] = {}
            for vname in os.listdir(diff_dir):
                if not vname.startswith("v") or not vname[1:].isdigit():
                    continue
                ver = int(vname[1:])
                path = os.path.join(diff_dir, vname, "trials.jsonl")
                if not os.path.exists(path):
                    continue
                trials = []
                with open(path) as f:
                    for line in f:
                        if line.strip():
                            try:
                                trials.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass
                if trials:
                    results[test][diff][ver] = trials
    return results


def summarize(trials):
    """Count judgments in a trial list."""
    counts = {"correct": 0, "abstained": 0, "confident_wrong": 0, "format_error": 0}
    for t in trials:
        j = t.get("judgment", "format_error")
        counts[j] = counts.get(j, 0) + 1
    return counts


def print_table(results, version="latest"):
    header = f"{'Test':<28} {'Diff':<8} {'Ver':<4} {'N':>4} {'✓':>4} {'?':>4} {'✗':>4} {'!':>4} {'Acc':>6}"
    print(f"\n{header}")
    print("-" * len(header))

    for test in sorted(results):
        for diff in ["easy", "medium", "hard"]:
            if diff not in results[test]:
                continue
            versions = results[test][diff]
            if not versions:
                continue
            v = max(versions) if version == "latest" else int(version)
            if v not in versions:
                continue
            trials = versions[v]
            n = len(trials)
            c = summarize(trials)
            acc = c["correct"] / n * 100 if n > 0 else 0
            print(
                f"{test:<28} {diff:<8} v{v:<3} {n:>4} "
                f"{c['correct']:>4} {c['abstained']:>4} {c['confident_wrong']:>4} {c['format_error']:>4} "
                f"{acc:>5.1f}%"
            )


def print_grouped(results, taxonomy_path, version="latest"):
    with open(taxonomy_path) as f:
        taxonomy = json.load(f)
    for group, test_names in taxonomy.items():
        print(f"\n{'=' * 40}")
        print(f"  {group}")
        print(f"{'=' * 40}")
        grouped = {t: results[t] for t in test_names if t in results}
        if grouped:
            print_table(grouped, version)
        else:
            print("  (no results)")


def compare_versions(results, test_name, v1, v2):
    if test_name not in results:
        print(f"Test '{test_name}' not found.")
        return
    print(f"\nComparing {test_name}: v{v1} vs v{v2}")
    print(f"{'Diff':<8} {'v' + str(v1):>10} {'v' + str(v2):>10} {'Delta':>8}")
    print("-" * 40)
    for diff in ["easy", "medium", "hard"]:
        if diff not in results[test_name]:
            continue
        versions = results[test_name][diff]
        if v1 not in versions or v2 not in versions:
            missing = [v for v in [v1, v2] if v not in versions]
            print(f"{diff:<8}  (v{missing[0]} missing)")
            continue
        t1, t2 = versions[v1], versions[v2]
        a1 = sum(1 for t in t1 if t["judgment"] == "correct") / len(t1) * 100
        a2 = sum(1 for t in t2 if t["judgment"] == "correct") / len(t2) * 100
        print(f"{diff:<8} {a1:>9.1f}% {a2:>9.1f}% {a2 - a1:>+7.1f}%")


def main():
    p = argparse.ArgumentParser(description="Analyze Phase 3 results")
    p.add_argument("--model", required=True)
    p.add_argument("--taxonomy", help="Path to taxonomy JSON file")
    p.add_argument("--compare", nargs=2, type=int, metavar=("V1", "V2"))
    p.add_argument("--test", help="Specific test (for --compare)")
    p.add_argument("--version", default="latest")
    p.add_argument("--results-dir", default="results")
    args = p.parse_args()

    slug = args.model.replace(":", "_").replace("/", "_")
    model_dir = os.path.join(args.results_dir, slug)
    if not os.path.isdir(model_dir):
        print(f"No results for {args.model} at {model_dir}")
        sys.exit(1)

    results = load_results(model_dir)
    if not results:
        print("No results found.")
        sys.exit(1)

    if args.compare and args.test:
        compare_versions(results, args.test, args.compare[0], args.compare[1])
    elif args.taxonomy:
        print_grouped(results, args.taxonomy, args.version)
    else:
        print_table(results, args.version)


if __name__ == "__main__":
    main()
