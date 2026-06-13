# Model as Reader

Matching frontier LLM accuracy with small open-source models via deterministic orchestration and graph-structured retrieval.

**Paper**: [arXiv link placeholder]

## Thesis

An on-device 8B model can match frontier model accuracy on structured multi-hop knowledge retrieval by externalizing reasoning to a temporal knowledge graph and deterministic orchestrator. The model's only job: read 2-20 pre-selected facts, answer one direct question.

## Results

| Condition | Accuracy | Facts Seen |
|---|---|---|
| 8B orchestrated | 13/13 | ~14 / 200 |
| 8B single-shot | 11-12/13 | 200 / 200 |
| Sonnet orchestrated | 12/13 | 11 / 200 |
| Sonnet single-shot | 12/13 | 200 / 200 |

## Repository Structure

```
paper/
  main.tex                    # LaTeX source

phase1/
  phase1-orchestrator.jsx     # Browser artifact (React) — architecture validation
                              # Three conditions against Claude Sonnet via API

phase2/
  phase2.py                   # Local model validation via Ollama
                              # Self-contained, zero dependencies beyond stdlib

phase3/                       # Capability profiling harness (26 tests, 1560 trials)
  [NOT YET INCLUDED]          # To be added before submission

docs/
  01-goal.md                  # Thesis, success criteria, probability estimates
  02-journey.md               # Full experiment history
  00-handoff.md               # Session resumption document
  phase2-results.md           # Phase 2 findings
  phase3-session-summary.md   # Phase 3 session narrative
  phase3-milestone.md         # Full project milestone document
```

## Running Phase 2

Requires [Ollama](https://ollama.ai) running locally.

```bash
ollama pull llama3.1:8b
python3 phase2/phase2.py --model llama3.1:8b --scale 2 -v
```

### Options

- `--model`: Ollama model name (default: `llama3.1:8b`)
- `--scale`: Corpus size — 0 (60 facts), 1 (120), 2 (200, default)
- `--conditions`: `single-shot`, `orchestrated`, or both
- `-v`: Verbose logging

## Phase 1

React browser artifact designed for Claude.ai's artifact environment. Calls the Anthropic API from the browser. Running independently requires a React setup with API authentication.

## Scope

Entity-relationship queries over structured data with temporal updates. Synthetic benchmark (200 facts, 13 questions). See paper Limitations section.

## License

MIT

## Citation

```bibtex
@article{manoj2026modelasreader,
  title={Model as Reader: Matching Frontier LLM Accuracy with Small
         Open-Source Models via Deterministic Orchestration and
         Graph-Structured Retrieval},
  author={Manoj M},
  year={2026},
  note={arXiv preprint}
}
```
