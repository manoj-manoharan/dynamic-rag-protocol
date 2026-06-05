# Phase 3: Model Capability Profile

Test harness for profiling small model reliability as a reader and ingester.
No dependencies beyond Python 3.8+ and Ollama.

## Run

```bash
# Pull model
ollama pull gemma2:2b

# Run all tests
cd phase3
python run.py --model gemma2:2b

# Run specific tests
python run.py --model gemma2:2b --tests negation,simple_extraction

# Specific difficulty
python run.py --model gemma2:2b --tests negation --difficulty hard

# Parallel (match to your GPU capacity)
python run.py --model gemma2:2b --concurrency 4

# Create new version (after changing a generator)
python run.py --model gemma2:2b --tests negation --new-version

# Retry cells that had confident_wrong results
python run.py --model gemma2:2b --retry-failed

# Verbose logging
python run.py --model gemma2:2b -v
```

## Analyze

```bash
# Flat table
python analyze.py --model gemma2:2b

# Group by taxonomy
python analyze.py --model gemma2:2b --taxonomy taxonomies/example.json

# Compare versions
python analyze.py --model gemma2:2b --test negation --compare 1 2
```

## Add a test

1. Create `generators/your_test.py` with a `generate(difficulty, trial, seed)` function
2. Import and register it in `generators/__init__.py`
3. Run it: `python run.py --model gemma2:2b --tests your_test`

No changes to run.py needed.

## Results structure

```
results/{model}/{test}/{difficulty}/v{N}/
    trials.jsonl   # one JSON line per trial
    meta.json      # version metadata
```

Resume is automatic. Kill and restart anytime.
