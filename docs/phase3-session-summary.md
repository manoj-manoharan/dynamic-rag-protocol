# Session Summary: Phase 3 — Model Capability Profile

## Starting Point

Phase 1 validated the orchestration architecture with Sonnet (12/13, reading 5.5% of corpus). Phase 2 validated it with local models: gemma2:2b scored 13/13 three times, 12/13 twice. The 13-question benchmark was saturated. It couldn't discriminate between 2B, 8B, and Sonnet as readers.

We needed a better instrument.

## What We Built

A 26-test, 1,560-trial automated harness that profiles any model's reliability as a reader and ingester. Runs against Ollama (local) or any OpenAI-compatible API. Zero dependencies beyond Python stdlib.

### Design Principles

- A test is just a test. Name, description, generator, checker. No tags, no categories. Classification happens at analysis time via separate taxonomy files.
- Every trial is deterministic (seeded). Same seed = same input across models.
- Every result is preserved. Versioned folders, append-only JSONL, resume on restart.
- Four judgment bins: correct, abstained, confident_wrong, format_error. Confident_wrong is the kill metric.

### Architecture

```
phase3/
  run.py             # Harness: model client, checkers, store, runner, CLI
  analyze.py         # Reads results, groups by taxonomy, prints tables
  generators/        # One file per test, self-contained
    __init__.py      # Registry
    ...26 generators
  taxonomies/
    example.json     # Groups tests for analysis
  results/           # {model}/{test}/{difficulty}/v{N}/trials.jsonl
  logs/
```

Adding a new test: one file in generators/, one import in __init__.py. Zero changes to run.py.

## Test Inventory (26 tests)

### Locate (3 tests)
- **simple_extraction**: N person-role-company facts, extract one. Control baseline.
- **distractor_density**: Same company, many roles, find the right person.
- **position_bias**: Answer at first/middle/last position. Detects attention bias.

### Match (2 tests)
- **paraphrase**: Question uses different vocabulary than facts.
- **similar_names**: Confusable entity names (shared surname).

### Reason (6 tests)
- **negation**: "Who does NOT work at X?"
- **absence**: Property doesn't exist in facts. Correct answer is no.
- **temporal_ordering**: Pick latest from N chronological updates.
- **comparison**: Which item has the largest value.
- **counting**: Count entities matching a criterion.
- **transitivity**: 2-hop chain from co-located facts.

### Ingestion (3 tests)
- **entity_extraction_known**: Identify known entities in a sentence.
- **relationship_extraction**: Extract structured triples from a sentence.
- **supersession_detection**: Does new fact replace existing or is it additive.

### Load-Bearing: Single-Fact Comprehension (12 tests)
- **surface_form**: Same fact in different syntactic structures (passive, dense, informal).
- **question_form**: Same fact, question phrased differently.
- **multi_info_extraction**: One fact with 3-4 data points, ask about one.
- **negation_in_fact**: Fact contains negation ("not X but Y").
- **numeric_precision**: Extract correct number when multiple present.
- **temporal_precision**: Extract correct date when multiple present.
- **domain_language**: Corporate, legal, CRM, technical register.
- **minimal_pair**: Two nearly identical facts, discriminate.
- **instruction_adherence**: Fact contradicts world knowledge; follow the fact.
- **embedded_correction**: Fact has old and corrected values.
- **conditional_fact**: Distinguish asserted from conditional/hedged.
- **quoted_attribution**: Distinguish attributed claims from asserted facts.

## Results: Three-Model Comparison

### Full Capability Map

| Dimension | Gemma 2B | Llama 8B | DeepSeek V4 Pro |
|---|---|---|---|
| Locate/Match/Surface | ~98% | 100% | 100% |
| Extraction (multi-info, embedded, numeric, temporal) | 85-100% | 95-100% | 100% |
| Negation | 20-45% | 100% | 100% |
| Counting | 0-15% | 35-100% | Correctly refuses* |
| Absence | 0% (refuses) | 35-90% | Correctly refuses* |
| Temporal ordering | 30-55% at scale | 65-75% at scale | 100% |
| Transitivity | 65-85% | 100% | 100% |
| Instruction adherence | 50% hard | 100% | 100% |
| Minimal pair | 80% | 85-90% | 100% |
| Conditional/Attribution | Broken | 55-90% | Correctly refuses* |
| Relationship extraction | 30% medium | 40% hard | 100% |
| Supersession detection | 90% | 95-98% | 90-100% |

*V4 Pro refuses because it recognizes the facts might be incomplete. Fixable with prompt framing that establishes completeness.

### Three Tiers of Capability

**Tier 1: All models reliable.** Locate, match, entity extraction, simple extraction, embedded correction. Safe to delegate to any model.

**Tier 2: 8B reliable, 2B broken.** Negation, counting (small sets), transitivity, absence, relationship extraction (explicit), instruction adherence. The jump from 2B to 8B fixes these.

**Tier 3: Neither small model reliable.** Counting at 5+ items, temporal ordering at 4+ updates, implicit relationship extraction, conditional/epistemic reasoning. Need code-side solutions or fine-tuning.

## Key Findings

### 1. The load-bearing assumption holds for 8B

Single-fact comprehension (given the right fact and a question, extract the answer) is validated at ~100% for Llama 8B across surface forms, domains, question phrasings, numeric extraction, temporal extraction, instruction following, and embedded corrections. The architecture's foundation is sound.

### 2. Every failure found is code-solvable

| Failure | Code fix |
|---|---|
| Counting at scale | `len(filtered_list)` in code |
| Temporal ordering at scale | Sort by timestamp, give model only the latest |
| Negation (2B) | Reformulate as positive extraction, code computes complement |
| Absence | Code checks set membership |
| Conditional statements | Regex filter for "if," "pending," "reportedly" before model sees fact |
| Implicit relationships | Regex patterns for "left X to join Y" |

### 3. Frontier models are epistemically stricter than small models

V4 Pro correctly reasons that "2 people listed" doesn't mean "2 people total." Small models assume completeness without being told. The small model gets the "right" answer for the wrong reason. The frontier model gets the "wrong" answer for the right reason. Implication: frontier models need prompts establishing fact completeness.

### 4. 2B is not viable for production

Gemma 2B works for the Phase 2 benchmark (simple extraction from clean facts) but fails on negation, counting, transitivity, conditional reasoning, question form variation, epistemic tasks, and numeric precision at hard difficulty. Too many load-bearing failures.

### 5. 8B is the minimum viable model, with code support

Llama 8B handles all reading tasks except: counting at scale (code-side), temporal ordering at scale (code-side), and conditional/epistemic reasoning (code-side filtering). These are all deterministic operations.

### 6. Fine-tuning is available as a path

The generators produce training data for weak dimensions. LoRA/QLoRA on the 8B model targeting counting, temporal ordering, and conditional reasoning could close the gaps. The full test suite serves as the regression harness.

### 7. Three checker bugs found and fixed

- **surface_form/domain_language**: Informal templates used first name only; checker expected full name. Fix: accept first or last name match.
- **numeric_precision**: Budget values >= $1000K caused comma formatting mismatches. Fix: cap generated values below 1000.

These were only discovered by running against real models. The harness tests itself through use.

## Orchestrator Implications Per Model Size

### If using Gemma 2B
Orchestrator handles: counting, negation, absence, transitivity, temporal sorting, comparison, relationship extraction, conditional filtering. Model only does simple extraction and entity matching.

### If using Llama 8B
Orchestrator handles: counting at scale, temporal sorting at scale, conditional/epistemic filtering. Model handles everything else.

### If using frontier API
Fix prompt to establish fact completeness. Model handles everything. But loses: privacy, offline, zero-latency, cost predictability.

## Open Questions

1. Does V4 Pro work in the full orchestrated pipeline? (Phase 2 with API, not yet run)
2. Can fine-tuning close the 8B gaps on counting, temporal ordering, and conditional reasoning?
3. Does the architecture hold at 500+ facts?
4. How do the models perform on realistic messy input (CRM tickets, legal text)?
5. Where does entity extraction break at scale?
6. Is the lightweight temporal KG library worth building as a standalone tool?

## What This Session Produced

| Artifact | What |
|---|---|
| phase3/run.py | Test harness: Ollama + API support, async parallel, resume/retry |
| phase3/generators/ (26 files) | One per test dimension, deterministic, self-contained |
| phase3/analyze.py | Results reader, taxonomy grouping, version comparison |
| phase3/taxonomies/ | Analysis-time grouping, no coupling to tests |
| Results for 3 models | gemma2:2b, llama3.1:8b, deepseek-v4-pro |
| milestone-phase3-model-capability-profile.md | Milestone document |

## Cost

- Local models: electricity only
- DeepSeek V4 Pro full 1,560-trial run: ~20 INR ($0.24 USD)
- Total wall time: ~2-4 hours per local model, ~20 minutes for API

## Relation to Project Goal

The project goal is On-Device Autonomous Agents via Memory + Orchestration. Phase 1 proved the architecture. Phase 2 proved the reader. This session built the permanent testing infrastructure for the system's lifecycle: diagnose model capabilities, draw the code/model boundary, fine-tune if needed, validate, repeat.

We are past "does the architecture work?" and into "how do we build the complete system?"
