# Journey: From Thesis to Validated Architecture

## Starting Point

The hypothesis: with proper memory, we can offload complex reasoning to deterministic workflows and only rely on models for what they're best at — predicting the next thing based on context. Small reasoning models + memory should match frontier models.

The initial framing used a mental model of graph traversal: traversal handled deterministically, but the next node to traverse to handled by the model.

## Experiment 1: Memory as Accumulator (FAILED)

**What we built**: Three conditions (single-shot, memory-guided, constrained-memory) on a dimension-comparison task. Memory was a JSON object updated between steps.

**Result**: Single-shot scored 12/12 on all tasks. Memory conditions used 5-13x MORE tokens for identical accuracy.

**Why it failed**: The task wasn't hard enough. Sonnet handles 12-dimension comparisons trivially in one pass. Memory added overhead for zero gain.

**Key learning**: The first experiment failed because I built memory as an accumulator (every fact loaded through the model in batches, memory JSON re-sent every step). This contradicted the thesis. Memory should reduce what the model sees, not duplicate it.

## Experiment 2: RAG Paradigm Comparison (SUCCEEDED)

**What we built**: Four retrieval paradigms on a synthetic tech ecosystem corpus (60/120/200 facts) with multi-hop chains, override tracking, and noise.

### Conditions
- **Single-shot**: all facts dumped in context
- **Naive RAG**: keyword match, top-K facts
- **HippoRAG**: graph traversal (BFS), retrieve connected facts
- **GraphRAG**: community detection + LLM-generated summaries

### Results (200 facts)

| Condition | Accuracy | Avg Tok/Q | Facts Retrieved |
|---|---|---|---|
| Single Shot | 12/13 (92%) | 6,922 | 200 / 200 |
| Naive RAG | 7/13 (54%) | 4,445 | 15 / 200 |
| HippoRAG v1 (BFS) | 11/13 (85%) | 4,587 | 24 / 200 |
| GraphRAG v2 (expanded) | 12/13 (92%) | 5,544 | summaries |

### Key Findings

1. **Naive RAG is structurally broken for multi-hop**. It can't find intermediate entities not in the question text. This alone justifies graph-based retrieval.
2. **HippoRAG BFS** achieved 85% accuracy reading 12% of the corpus. Best efficiency.
3. **GraphRAG v2** matched single-shot accuracy using pre-digested community summaries.
4. **PPR was wrong for this graph scale** (54 nodes). BFS was better because the graph is small enough that "visit everything within 3 hops" IS the answer. PPR penalizes distance, which hurts when the answer IS distant.
5. **Single-shot degrades as corpus grows** (100% at 60 facts → 92% at 200). Retrieval methods stay flat.

### Algorithm Iterations

| Version | Accuracy | What Changed |
|---|---|---|
| HippoRAG v1 (BFS 3-hop) | 11/13 | Original implementation |
| HippoRAG v2 (PPR α=0.15) | 7/13 | PPR too selective, top-K cutoff too aggressive |
| HippoRAG v2.1 (PPR α=0.10, all scores) | 9/13 | Better but still worse than BFS |
| GraphRAG v1 (basic communities) | 11/13 | Basic label propagation + basic summaries |
| GraphRAG v2 (expanded retrieval) | 12/13 | Weighted communities + 1-hop expanded matching + structured summary prompt |

**Lesson**: PPR is designed for large graphs (10K+ nodes). At 54 nodes, BFS is better. The right algorithm depends on graph scale.

## Experiment 3: Memory + Orchestration (SUCCEEDED)

**What we built**: Deterministic orchestrator that uses KG structure to decompose questions and retrieve only path-edge facts. Three conditions, all using Sonnet.

### Conditions
- **A: Single Shot**: all 200 facts, one call
- **B: Path Retrieval**: KG-guided, only path-edge facts, one call
- **C: Step-by-Step**: one hop at a time with working memory

### Bug Discovery and Fix Cycle

Initial B and C scored 8/13 (62%). Detailed logging revealed four bugs:

1. **Misclassification**: "Name the sibling of Quantum Labs' founder" classified as "direct" instead of "chain" (regex didn't handle `s'` possessive). "Does anyone at Vertex have a family member..." missed by keyword patterns.
2. **BFS shortest-path bias**: Found corporate shortcut (NexGen→Orion, 1 hop via partnership) instead of personal chain (NexGen→Sarah→James→Orion, 3 hops via marriage).
3. **Context fact bloat**: After finding path, code pulled ALL facts about ALL path entities (33-43 facts) instead of just path-edge facts (3-5 facts).
4. **Ground truth too narrow**: Forge→Apex check only accepted one valid chain when two existed.

### Fixes Applied
1. Extended classification regex patterns
2. Replaced single-path BFS with multi-path DFS (returns ALL paths up to 5 hops)
3. Stripped context facts — return ONLY path-edge facts
4. Accepted both valid chains in ground truth

### Final Results (200 facts)

| Condition | Accuracy | Avg Facts Seen | Avg Tok/Q |
|---|---|---|---|
| A: Single Shot | 12/13 (92%) | 200 / 200 | 6,919 |
| **B: Path Retrieval** | **12/13 (92%)** | **11 / 200** | **4,399** |
| C: Step-by-Step | 12/13 (92%) | 11 / 200 | 11,600 |

**B matches A reading 5.5% of the corpus, using 36% fewer tokens.** The graph does the multi-hop reasoning. The model just reads the answer from pre-selected facts.

**C adds no accuracy over B but costs 2.6x more tokens.** Step-by-step decomposition is unnecessary for Sonnet but is the mechanism that enables small models (Phase 2).

## Research Context

Searched for related work. The space is active:

- **HippoRAG** (NeurIPS 2024): hippocampus-inspired KG index. 10-30x cheaper than iterative retrieval.
- **GraphRAG** (Microsoft, 2024): community summaries for global sensemaking.
- **MemGPT** (2023): OS-inspired memory hierarchy for LLM agents.
- **Graphiti/Zep** (2025): temporal knowledge graph with incremental updates, bi-temporal model.
- **GBrain** (2025): zero-LLM-call wiring via regex patterns, markdown-native.
- **EVOREASONER**: 8B model matching 671B model using temporal KG + multi-hop decomposition.

**Gap identified**: No lightweight, embeddable temporal KG exists as a data structure. Everything is a framework (requires Neo4j, Postgres, or specific file structures). The abstract primitive underneath all of them is the same: a temporal property graph with versioned edges, entity-keyed indexing, and traversal-based retrieval.

## Architecture Design: Two-Tier Memory

Derived from experiments and literature:

```
Orchestrator (deterministic code)
  ├── classifies question type
  ├── extracts entities (string matching)
  ├── finds paths via multi-path DFS in KG
  ├── retrieves only path-edge facts (4-8 facts)
  ├── feeds [working memory + retrieved facts] to model
  ├── stores result in working memory
  └── after task: consolidates new facts to KG

Working Memory (JSON in RAM, per-task)
  ├── goal, current step, resolved answers, pending steps
  └── discarded after task completion

Long-Term Memory (Temporal KG, persistent)
  ├── entity nodes with versioned properties
  ├── relationship edges with timestamps
  ├── supersession: new edge auto-closes previous
  └── updated periodically, not during reasoning

Small Model (8B, on-device)
  └── only does: read 2-8 facts → produce one answer
```
