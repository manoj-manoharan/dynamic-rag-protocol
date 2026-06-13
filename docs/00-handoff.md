# Handoff: Memory-Enabled Autonomous Agents

## What This Is

An experiment proving that an on-device 8B model can match frontier model accuracy on multi-hop knowledge retrieval by externalizing reasoning to a temporal knowledge graph + deterministic orchestrator.

## Where We Are

**Phase 1: DONE.** Architecture validated with Sonnet. Path retrieval matches single-shot (12/13 both) while reading 5.5% of the corpus.

**Phase 2: READY.** Python script written (`phase2.py`). Needs to be run locally with Ollama. Not yet executed.

## The Architecture That Works

```
Question → Extract entities (string match) → Classify question type
  ├── Connection: multi-path DFS finds ALL paths between entities (up to 5 hops)
  │     → retrieve ONLY path-edge facts (4-8 facts, not 200)
  │     → model reads facts, answers question
  ├── Chain (possessive): 1-hop neighbor expansion → model reads ~20 facts
  ├── Override: entity lookup → model reads ~13 facts (temporal, picks latest)
  ├── Aggregation: pattern match (e.g., all "acquired" facts) → model reads ~3 facts
  └── Direct: entity lookup → model reads relevant facts
```

Model's only job: read 2-20 pre-selected facts, answer one question. Graph handles multi-hop traversal. Code handles decomposition.

## Key Results

| Condition | Accuracy (200 facts) | Facts Seen | Tokens/Q |
|---|---|---|---|
| Sonnet single-shot | 12/13 (92%) | 200 | 6,919 |
| Sonnet orchestrated (path retrieval) | 12/13 (92%) | 11 | 4,399 |
| Sonnet step-by-step | 12/13 (92%) | 11 | 11,600 |
| 8B orchestrated | **NOT YET RUN** | 11 | ? |

## What Failed Along the Way

1. **Memory as accumulator** (Exp 1): loaded all facts through model in batches. 5-13x more tokens, no accuracy gain. Wrong architecture.
2. **PPR on small graphs** (Exp 2): Personalized PageRank worse than BFS at 54 nodes. PPR penalizes distance; BFS covers the small graph fully. PPR is for 10K+ node graphs.
3. **Single-path BFS** (Exp 3): found corporate shortcuts instead of personal chains. Fixed with multi-path DFS returning ALL paths.
4. **Context fact bloat** (Exp 3): pulled all facts about path entities (33+ facts) instead of just path-edge facts (4-8). Fixed by stripping context facts.

## Immediate Next Step

Run Phase 2 locally:

```bash
ollama pull llama3.1:8b
python3 phase2.py --model llama3.1:8b --scale 2 --conditions orchestrated -v
python3 phase2.py --model llama3.1:8b --scale 2 --conditions single-shot
```

**Success**: 8B orchestrated ≥ 10/13 (77%).
**Strong success**: 8B orchestrated > 8B single-shot (proves orchestration helps small models specifically).

## Corpus

Synthetic tech ecosystem. 200 facts at large scale: 15 companies, ~35 people, roles, marriages, siblings, acquisitions, partnerships, products, project budgets with multiple overrides, leadership changes with reversals. ~80 meaningful facts + ~120 noise facts.

13 questions at large scale: 3 direct, 3 override, 2 two-hop, 2 three-hop, 2 four-hop, 1 aggregation. Ground truth verified. Multi-hop chains require 3-5 hops through personal and corporate relationships.

## Files

| File | What |
|---|---|
| `phase2.py` | Phase 2 script. Run with Ollama. Self-contained. |
| `phase1-orchestrator.jsx` | Phase 1 browser experiment (validated architecture) |
| `rag-experiment-v2.jsx` | RAG paradigm comparison (HippoRAG vs GraphRAG vs Naive vs Single-shot) |
| `01-goal.md` | Thesis, success criteria, probability estimates |
| `02-journey.md` | Full experiment history with all results |
| `03-plan.md` | Roadmap, future directions, publishable story structure |

## Context Documents

For a new session, provide:
- **This handoff** (essential, always include)
- **01-goal.md** if discussing the thesis or scope
- **02-journey.md** if debugging or extending experiments
- **03-plan.md** if planning next steps or the writeup

## Open Questions

1. Does 8B orchestrated match Sonnet? (Phase 2, not yet run)
2. What's the smallest model that still works? (Phi-3 3.8B?)
3. Does the architecture hold at 500+ facts? (Token gap should widen, accuracy gap should too)
4. Can temporal updates be handled incrementally? (Graphiti does it, nobody has the lightweight version)
5. Is the lightweight temporal KG library worth building? (The portable primitive that Graphiti and GBrain both implement but nobody has extracted)
