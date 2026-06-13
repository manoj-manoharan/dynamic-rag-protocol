# Goal: On-Device Autonomous Agents via Memory + Orchestration

## Thesis

An on-device, open-source 8B model can match frontier model accuracy on structured knowledge retrieval tasks, enabled by:

1. **Two-tier memory**: working memory (active reasoning state) + temporal knowledge graph (persistent knowledge)
2. **Deterministic orchestration**: code decomposes complex tasks into single-hop steps the small model reliably executes
3. **Graph-based retrieval**: the KG routes queries to relevant facts, so the model never sees the full corpus

The model's only job is: read 2-8 facts, answer one direct question. Everything else is deterministic code.

## Core Insight

Distribution of labor between code and model:

- **Code handles**: task decomposition, graph traversal, entity extraction, path finding, temporal supersession, working memory management
- **Model handles**: reading retrieved facts and producing one answer per step

The model is never the planner, decomposer, or retriever. It is the reader.

## Scoped Claim

This architecture solves **structured knowledge retrieval over entity-relationship graphs with temporal updates**. Not general reasoning. Specific, valuable, well-defined category covering: customer data, project tracking, organizational knowledge, personal CRM, regulatory compliance.

## Success Criteria

| Metric | Threshold |
|---|---|
| 8B model orchestrated accuracy | ≥ 80% of Sonnet single-shot (≥10/13 on our benchmark) |
| Per-question token cost | < Sonnet single-shot |
| Per-step model complexity | Each step is a single-hop lookup |
| On-device, open-source | Runs via Ollama, no API calls |

## What Success Looks Like

A table showing an 8B local model matching Sonnet on multi-hop reasoning over a 200+ fact corpus, with a breakdown showing: the model never had to reason across more than one hop because the orchestration layer carried the chain.

## What Failure Looks Like and What It Means

- **8B fails on single-hop steps**: model isn't capable enough. Find the threshold (14B? 32B?).
- **Each step right but wrong final answer**: orchestrator decomposition is flawed. Fix code, not model.
- **Accuracy matches but costs more tokens**: architecture works but isn't economical. Reliability over efficiency is still a finding.
- **Negative result**: equally publishable if we characterize exactly where and why it fails.

## Honest Probability Estimate

| Claim | Probability |
|---|---|
| Architecture works (Sonnet orchestrated ≥ Sonnet single-shot) | **85% — VALIDATED** |
| 8B handles single-hop extraction reliably | 95% |
| Error compounding stays manageable (with verification) | 80% |
| 8B orchestrated matches Sonnet on our benchmark | 70% |
| Scoped goal (entity-relationship queries on structured data) | 65-70% |
