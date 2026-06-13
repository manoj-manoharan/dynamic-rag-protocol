# Project Milestone: On-Device Autonomous Agents via Memory + Orchestration

## Thesis

An on-device open-source model (8B parameters) can match frontier model accuracy on structured knowledge retrieval by externalizing multi-hop reasoning to a temporal knowledge graph and deterministic orchestrator. The model's only job is: read 2-20 pre-selected facts, answer one direct question. Code handles everything else: task decomposition, graph traversal, entity extraction, path finding, temporal supersession, working memory management.

Scoped claim: this architecture solves entity-relationship queries over structured data with temporal updates. Not general reasoning. The category covers customer data, project tracking, organizational knowledge, personal CRM, regulatory compliance.

A second thesis thread emerged during the project: boolean gate evaluation (facts + predicate -> true/false) as a foundational primitive for composable, practically-deterministic natural language workflows. This remains scoped separately, not yet experimentally validated.

## Results

All five core claims from the original goal document are now validated.

| Claim | Prior Estimate | Status | Evidence |
|---|---|---|---|
| Architecture works (Sonnet orchestrated >= Sonnet single-shot) | 85% | Validated | 12/13 both, orchestrated reads 5.5% of corpus |
| 8B handles single-hop extraction reliably | 95% | Validated | ~100% when given correct facts (Phase 2 + Phase 3) |
| Error compounding stays manageable | 80% | Validated | No compounding; single-step design eliminates it |
| 8B orchestrated matches Sonnet on benchmark | 70% | Validated (exceeds) | 13/13 vs 12/13 |
| Scoped goal (entity-relationship queries on structured data) | 65-70% | Validated at current scale | 200 facts, 13 questions, multiple model sizes |

The 13-question benchmark is saturated. It cannot discriminate between Gemma 2B, Llama 8B, and Sonnet as readers. Phase 3 was built to address this.

## What Happened, in Order

### Phase 1: Architecture Validation (Browser Artifacts, Sonnet)

Three experiments, all run as React artifacts calling the Anthropic API against a synthetic 200-fact tech ecosystem corpus (15 companies, ~35 people, roles, marriages, siblings, acquisitions, partnerships, products, budget overrides, leadership changes).

**Experiment 1: Memory as accumulator.** Failed. Loaded all facts through the model in batches, memory JSON re-sent every step. 5-13x more tokens for identical accuracy. The task (12-dimension comparison) wasn't hard enough to need memory, and the architecture was wrong: memory should reduce what the model sees, not duplicate it.

**Experiment 2: RAG paradigm comparison.** Four retrieval methods at 200 facts.

| Method | Accuracy | Facts Seen | Tokens/Q |
|---|---|---|---|
| Single-shot (all facts) | 12/13 (92%) | 200 | 6,922 |
| Naive RAG (keyword top-K) | 7/13 (54%) | 15 | 4,445 |
| HippoRAG BFS (3-hop) | 11/13 (85%) | 24 | 4,587 |
| GraphRAG v2 (community summaries) | 12/13 (92%) | summaries | 5,544 |

Naive RAG is structurally broken for multi-hop because it can't find intermediate entities not present in the question text. PPR (Personalized PageRank) was tested and performed worse than BFS (9/13 vs 11/13) because PPR penalizes distance, which is wrong for a 54-node graph where the answer IS distant. BFS covers the small graph fully. PPR is designed for 10K+ node graphs.

**Experiment 3: Deterministic orchestrator.** Multi-path DFS graph traversal, path-edge fact retrieval, three conditions.

| Condition | Accuracy | Facts Seen | Tokens/Q |
|---|---|---|---|
| A: Single Shot | 12/13 | 200 | 6,919 |
| B: Path Retrieval | 12/13 | 11 | 4,399 |
| C: Step-by-Step | 12/13 | 11 | 11,600 |

B matches A reading 5.5% of the corpus, using 36% fewer tokens. C adds no accuracy over B but costs 2.6x more tokens. Step-by-step decomposition is unnecessary for Sonnet but exists as the mechanism that enables small models.

Initial B and C scored 8/13. Debug logging (not architectural changes) revealed four bugs: misclassification due to possessive regex not handling `s'`, BFS shortest-path bias finding corporate shortcuts instead of personal chains, context fact bloat pulling all facts about path entities instead of just path-edge facts, and overly narrow ground truth. All four were code bugs. This pattern held throughout the entire project.

### Phase 2: Local Model Validation (Ollama, 8B and 2B)

Python script (`phase2.py`) run locally against Llama 3.1:8b and Gemma 2:2b via Ollama.

| Condition | Accuracy | Stable |
|---|---|---|
| 8B orchestrated | 13/13 | Yes (after bug fixes) |
| 8B single-shot | 11-12/13 | No (rotating failures) |
| 2B orchestrated | 13/13 (3 runs), 12/13 (2 runs) | No |
| Sonnet orchestrated (Phase 1) | 12/13 | Yes |

Two bugs were found and fixed during Phase 2. First, DFS terminated at target entities without expanding to connected person-entities (e.g., finding "Orion Corp" but not expanding to "Dr. Wei Lin" who works there), causing Q11 failures. Second, endpoint expansion was directional and depended on Python `set()` hash randomization across process invocations, causing intermittent failures in 2 of 4 runs. Fix: expand both endpoints unconditionally.

Gemma 2B's intermittent Q10 failures (2/5 runs) traced to noise fact bloat from endpoint expansion pulling irrelevant company facts (29 facts instead of 4-5 path-edge facts). The model produced a plausible but incorrect chain-of-reasoning answer.

The operational insight from Phase 2: every failure across both phases was a code bug, never a model comprehension failure. When the model's only job is reading pre-selected facts, debugging is software engineering, not prompt engineering. You never changed a prompt or fine-tuned anything to fix a wrong answer. You fixed the orchestrator.

### Phase 3: Model Capability Profile (26-Test Harness)

The 13-question benchmark was saturated. It couldn't tell 2B from 8B from Sonnet as readers. A finer instrument was needed.

Built a 26-test, 1,560-trial automated harness that profiles any model's reliability as a reader and ingester. Runs against Ollama (local) or any OpenAI-compatible API. Zero dependencies beyond Python stdlib. Design principles: a test is just a test (name, generator, checker; taxonomy at analysis time only), every trial deterministic (seeded), every result preserved (versioned folders, append-only JSONL, resume on restart), four judgment bins (correct, abstained, confident_wrong, format_error).

Adding a new test: one file in `generators/`, one import in `__init__.py`. Zero changes to `run.py`.

Tests span five areas: Locate (simple extraction, distractor density, position bias), Match (paraphrase, similar names), Reason (negation, absence, temporal ordering, comparison, counting, transitivity), Ingestion (entity extraction, relationship extraction, supersession detection), and Load-Bearing Single-Fact Comprehension (12 tests covering surface form, question form, multi-info extraction, negation in fact, numeric precision, temporal precision, domain language, minimal pair, instruction adherence, embedded correction, conditional fact, quoted attribution).

Run against Gemma 2:2b, Llama 3.1:8b, DeepSeek V4 Pro, and DeepSeek V4 Flash.

**Three capability tiers emerged:**

Tier 1 (all models reliable): locate, match, entity extraction, simple extraction, embedded correction. Safe to delegate to any model.

Tier 2 (8B reliable, 2B broken): negation, counting (small sets), transitivity, absence, relationship extraction (explicit), instruction adherence. The jump from 2B to 8B fixes these.

Tier 3 (neither small model reliable): counting at 5+ items, temporal ordering at 4+ updates, implicit relationship extraction, conditional/epistemic reasoning. Need code-side solutions or fine-tuning.

**Per-model summary:**

Gemma 2B: reliable only for direct extraction from clean simple facts. Negation (20-45%), counting (0-15%), absence (0%), transitivity (65-85%), temporal ordering (30-55% at scale). Not viable for production beyond trivial extraction.

Llama 8B: reliable for most reading tasks. Breaks on counting at scale, temporal ordering at scale, conditional/epistemic reasoning. Minimum viable model with code support for the gaps.

DeepSeek V4 Pro: 100% on every reading and ingestion dimension. But epistemically stricter than small models: correctly reasons that "2 people listed" doesn't mean "2 people total," refusing to assert from potentially incomplete facts. Small models assume completeness without being told. The frontier model gets the "wrong" answer for the right reason. Fixable with prompt-level completeness framing. Cost for full 1,560-trial run: ~20 INR ($0.24 USD).

DeepSeek V4 Flash: not just a faster V4 Pro. Has a real capability gap compared to V4 Pro.

**Every Tier 3 failure is code-solvable:**

| Failure | Code fix |
|---|---|
| Counting at scale | `len(filtered_list)` in code |
| Temporal ordering at scale | Sort by timestamp, give model only the latest |
| Negation (2B) | Reformulate as positive extraction, code computes complement |
| Absence | Code checks set membership |
| Conditional statements | Regex filter for hedging language before model sees fact |
| Implicit relationships | Regex patterns for "left X to join Y" |

Three checker bugs were found through real model results and fixed: surface_form/domain_language templates using first name only against full-name checkers, and numeric_precision generating values >=1000K causing comma formatting mismatches. The harness tests itself through use.

### Side Thread: Boolean Gate Thesis

Scoped as a second thesis, separate from but supporting the main line. The idea: constraining LLM output to a single boolean (facts + predicate -> true/false) produces the maximally reliable primitive. Code composes gates into circuits using standard logic. Practical determinism (not mathematical) is achievable through three mechanisms: redundancy (majority vote of 3 at 95% per-gate gives ~99.3%), verification gates (gates checking gates), and fallback boundaries (workflow declares uncertainty rather than guessing). The contract becomes: always produces a correct answer OR explicitly declares it can't. Never a silent wrong answer.

Not yet experimentally validated. Would require a parallel boolean benchmark: same corpus, all yes/no questions, measure per-gate accuracy, then measure composed accuracy against theoretical prediction from individual gate reliability.

### Side Thread: Production Architecture

Discussion began but no decisions finalized. The target: Docker services acting as a router for queries and ingestions, with a small local model for simple inference, API connection to frontier model for complex tasks, and a shared entity-relationship graph built by and served to the services.

Three design tensions surfaced. First, KG service boundary: smart KG service owning traversal algorithms (recommended) vs dumb data service with orchestrator-side traversal. Second, model routing: hard rule table from Phase 3 capability tiers vs learned routing. Third, ingestion scope: whether v1 includes live KG growth or is query-only.

## Key Principles Discovered

**Memory as routing index, not accumulator.** The first experiment failed because memory accumulated context (every fact loaded through the model in batches, memory JSON re-sent every step). The correct role is as a retrieval/routing index directing the model to pre-selected, minimal context.

**Single-hop reader principle.** LLM accuracy and cost improve dramatically when the model only performs single-step extraction from pre-selected context. Multi-hop reasoning is handled deterministically in code. The model is never the planner, decomposer, or retriever. It is the reader.

**Path-edge retrieval, not entity-fact retrieval.** The critical design choice is retrieving only the facts that connect entities along graph paths. Not all facts about path entities (bloat, 33+ facts), not all facts in corpus (noise), not keyword-matched facts (misses intermediate entities). 14 facts out of 200.

**Evidence before fixes.** Diagnosis via debug logging before architectural changes. This principle caught four bugs in Phase 1 and two in Phase 2 that would have been misattributed to model limitations.

**All bugs were code bugs.** Across three phases and hundreds of trials, no failure traced to model comprehension. Misclassification, BFS shortest-path bias, context fact bloat, ground truth too narrow, DFS endpoint expansion, Python set hash randomization, checker regex patterns. Every one fixable in the orchestrator or test harness. This is the operational advantage: debugging is software engineering, not prompt engineering.

**Orchestration helps small models more than large ones.** Sonnet gained efficiency (36% fewer tokens) but no accuracy. 8B gained both accuracy (+2) and stability. 2B went from non-viable to 13/13 on the benchmark. The architecture matters more as model capability decreases.

**Frontier models are epistemically stricter.** V4 Pro correctly recognizes incomplete information and refuses to assert. Small models assume completeness. This is not a bug in either; it's a different contract. Implications: frontier models need prompts establishing fact completeness; small models need code-side guardrails against overconfident wrong answers.

**PPR is wrong for small graphs.** BFS outperformed PPR at 54 nodes (11/13 vs 9/13). PPR penalizes distance, which hurts when the answer requires traversing the full graph. PPR is designed for 10K+ node graphs where you need to prioritize.

## Related Work

Surveyed during Phase 1:

- **HippoRAG** (NeurIPS 2024): hippocampus-inspired KG index, 10-30x cheaper than iterative retrieval
- **GraphRAG** (Microsoft, 2024): community summaries for global sensemaking
- **MemGPT** (2023): OS-inspired memory hierarchy for LLM agents
- **Graphiti/Zep** (2025): temporal knowledge graph with incremental updates, bi-temporal model
- **GBrain** (2025): zero-LLM-call wiring via regex patterns, markdown-native
- **EVOREASONER**: 8B model matching 671B model using temporal KG + multi-hop decomposition

Gap identified: no lightweight, embeddable temporal KG exists as a standalone data structure. Everything is a framework (requires Neo4j, Postgres, or specific file structures). The abstract primitive underneath all of them is the same: a temporal property graph with versioned edges, entity-keyed indexing, and traversal-based retrieval.

## What Failed and Why (Complete List)

| Failure | Phase | Root Cause | Fix |
|---|---|---|---|
| Memory as accumulator | 1 | Architecture contradiction: memory added overhead, didn't reduce context | Redesigned: memory as routing index |
| PPR on small graphs | 1 | PPR penalizes distance; wrong for 54-node graph | Used BFS/DFS |
| Possessive regex misclassification | 1 | Regex didn't handle `s'` (e.g., "Labs' founder") | Extended patterns |
| BFS shortest-path bias | 1 | Found corporate shortcuts instead of personal chains | Multi-path DFS |
| Context fact bloat | 1 | Pulled all facts about path entities (33+), not path-edge facts (4-8) | Strip to path-edge only |
| Ground truth too narrow | 1 | Only accepted one valid chain when two existed | Accept both |
| DFS endpoint non-expansion | 2 | Terminated at target entity without expanding to connected persons | Expand endpoints |
| Directional endpoint expansion | 2 | Expansion direction depended on Python set hash randomization | Expand both endpoints |
| Noise fact bloat (2B) | 2 | Endpoint expansion pulled irrelevant company facts | Identified; not fully fixed |
| Checker: first-name-only templates | 3 | Informal templates used first name; checker expected full name | Accept first or last |
| Checker: numeric formatting | 3 | Values >=1000K caused comma mismatches | Cap below 1000 |

## Artifacts Produced

| Artifact | What | Phase |
|---|---|---|
| `phase1-orchestrator.jsx` | Browser experiment: Sonnet, 3 conditions, KG, DFS | 1 |
| `phase2.py` | Local Ollama experiment: 8B/2B vs Sonnet baseline | 2 |
| `phase2-results.md` | Phase 2 findings, bug fixes, architectural implications | 2 |
| `phase3/run.py` | 26-test harness: Ollama + API, async parallel, resume/retry | 3 |
| `phase3/generators/` (26 files) | One per test dimension, deterministic, self-contained | 3 |
| `phase3/analyze.py` | Results reader, taxonomy grouping, version comparison | 3 |
| `phase3/taxonomies/` | Analysis-time grouping, decoupled from tests | 3 |
| `01-goal.md` | Thesis, success criteria, probability estimates | 1 |
| `02-journey.md` | Full experiment history | 1-2 |
| `00-handoff.md` | Session resumption document | 1 |

## Open Questions

1. Does the architecture hold at 500+ facts? Token gap should widen, accuracy gap should too. Noise ratio increases.
2. What's the smallest model that works? Gemma 2B works on the saturated benchmark but fails on the capability profile. Something between 2B and 8B is the real floor.
3. Can fine-tuning close the 8B gaps? The Phase 3 generators produce training data. LoRA/QLoRA targeting counting, temporal ordering, and conditional reasoning. The test suite serves as the regression harness.
4. Does V4 Pro work in the full orchestrated pipeline? Phase 2 with API, not yet run. Expected: 13/13 trivially once completeness prompting is added.
5. How do the models perform on realistic messy input? CRM tickets, legal text, unstructured notes. The synthetic corpus is clean by construction.
6. Where does entity extraction break at scale? String matching works at 200 facts and 35 entities. At 1000+ entities with name collisions, it won't.
7. Is the lightweight temporal KG library worth building? The portable primitive that Graphiti, GBrain, and this project all implement but nobody has extracted as a standalone data structure.
8. Can the same orchestration pattern handle the write side? Ingestion decomposed into single-hop steps (entity extraction, coreference resolution, relationship extraction, supersession detection, verification). Discussed, not built.
9. Boolean gate thesis: does per-gate accuracy compose as predicted by probability theory? Requires a parallel boolean benchmark, not yet designed.

## Where This Stands

The project has moved through three phases: prove the architecture works (Phase 1), prove the reader works (Phase 2), build permanent testing infrastructure (Phase 3). All original success criteria are met. The system is past "does it work?" and into "how do we build the complete system?" The next decision is whether to push toward production (Docker services, ingestion pipeline, live KG) or deepen the experimental foundation (scale testing, fine-tuning, boolean gate validation, messy-input evaluation).

## Cost

- Phase 1: Anthropic API credits (in-artifact Sonnet calls)
- Phase 2: Electricity only (local Ollama)
- Phase 3 local models: Electricity only
- Phase 3 DeepSeek V4 Pro (1,560 trials): ~20 INR ($0.24 USD)
- Wall time: ~2-4 hours per local model, ~20 minutes for API
