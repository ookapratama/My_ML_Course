# PROGRESS — Single Source of Truth

> This is the **one place** progress lives. Both `product-plan.md` (build) and
> `ai-engineering-learning-plan.md` (concepts) point here — do not keep separate checkboxes.
> Two streams move together per phase: **Learn** (lessons via `/learn-mode`) and **Build** (the artifact).
>
> **Sync rule:** when a lesson passes (`[LESSON_PASSED]`), tick its Learn box here. When a
> phase artifact runs and is measured, tick its Build box here. Nowhere else.

---

## Current position

- **Phase:** 0 — Foundations & scaffolding
- **Lesson:** none started yet
- **Next action:** scaffold repo + stand up local stack (Postgres + pgvector + n8n)

_Update these three lines at the end of every session._

---

## Phase 0 — Foundations & scaffolding
**Learn**
- [ ] Local stack mental model (why pgvector + n8n + FastAPI together)
- [ ] Swappable-interface pattern (`Embedder` / `LLMClient` / `Retriever` / `Tracer`)

**Build**
- [ ] Repo structure + `uv` env
- [ ] `docker-compose.yml` (Postgres + pgvector + n8n) comes up clean
- [ ] Interface stubs defined

**Artifact gate:** `docker compose up` brings the whole stack online.

---

## Phase 1 — Baseline RAG  ·  (concepts: Modules 1, 2, 3-intro, 4-core)
**Learn**
- [ ] M1 · tokens, context window, temperature/top-p
- [ ] M1 · prompting patterns
- [ ] M1 · streaming + response parse *(hand-code)*
- [ ] M2 · parsing real formats (JSON/CSV/HTML/PDF) *(hand-code a parser each)*
- [ ] M2 · data structures behind indexes (arrays, hash maps, trees/graphs)
- [ ] M3 · what an embedding is + cosine similarity *(hand-code once)*
- [ ] M3 · chunking strategies
- [ ] M4 · retrieve → augment → generate loop *(hand-code)*
- [ ] M4 · citations

**Build**
- [ ] Ingestion: parse → chunk → embed → index into pgvector
- [ ] Dense retrieval + generation with citations
- [ ] Typed `LLMClient` wrapper

**Artifact gate:** ask a question over a real corpus, get a cited answer.

---

## Phase 2 — Evaluation harness *(the differentiator)*  ·  (concepts: Module 4 eval)
**Learn**
- [ ] Why eval is the bottleneck; what "good" even means for RAG
- [ ] Golden dataset design (Q + ground-truth answer + relevant-chunk labels)
- [ ] Retrieval metrics: recall@k, precision@k, MRR, nDCG *(hand-code one)*
- [ ] Generation metrics: faithfulness, answer relevance, correctness, citation accuracy *(hand-code faithfulness)*
- [ ] LLM-as-judge + validating the judge against a heuristic baseline

**Build**
- [ ] Golden set (~30–50 pairs)
- [ ] Metric implementations
- [ ] `veritas eval` prints a scorecard for any config

**Artifact gate:** scorecard runs; every future change becomes measurable.

---

## Phase 3 — Hybrid retrieval + reranking  ·  (concepts: Module 3 deeper)
**Learn**
- [ ] BM25 / sparse retrieval intuition
- [ ] Reciprocal Rank Fusion *(hand-code the fusion)*
- [ ] Cross-encoder reranking (bi-encoder vs cross-encoder)
- [ ] Reading a metric delta: is an improvement real or noise?

**Build**
- [ ] BM25 + dense + RRF fusion
- [ ] Cross-encoder reranker
- [ ] Tune chunk size / top-k / weights against the scorecard

**Artifact gate:** before/after metrics table proving each addition helped.

---

## Phase 4 — Observability & tracing  ·  (concepts: Module 5 production)
**Learn**
- [ ] Spans / traces mental model
- [ ] What to capture: chunks, scores, prompt, tokens, latency, cost
- [ ] OpenTelemetry GenAI semantic conventions *(read once)*
- [ ] One end-to-end span written by hand *(hand-code)*

**Build**
- [ ] Trace store in Postgres
- [ ] Instrument every stage
- [ ] Minimal Vite dashboard to inspect any past request

**Artifact gate:** click an answer in the dashboard, see exactly why it happened.

---

## Phase 5 — Agentic self-correction  ·  (concepts: Module 5 agents)
**Learn**
- [ ] Tool/function-call schema *(hand-code)*
- [ ] Agent loop as a control system *(hand-code)*
- [ ] Context grading + query decomposition
- [ ] Answer grading + honest refusal
- [ ] Loop termination + cost ceiling

**Build**
- [ ] Context-sufficiency grader → re-query
- [ ] Answer grounding grader → retry / refuse
- [ ] Loop guards (max steps, cost cap)
- [ ] Measure agentic vs baseline on the scorecard (quality, cost, latency)

**Artifact gate:** multi-hop and unanswerable questions handled honestly.

---

## Phase 6 — Productionization & automation  ·  (concepts: Module 5 + 5b n8n)
**Learn**
- [ ] n8n data model: nodes, connections, expressions, credentials
- [ ] HTTP Request + Code nodes; webhook triggers
- [ ] Raw n8n workflow JSON *(hand-code/read once)*
- [ ] Guardrails, caching, rate limiting basics

**Build**
- [ ] n8n: upload → trigger ingestion
- [ ] n8n: nightly eval run → regression alert (Slack/email)
- [ ] n8n: webhook query entrypoint
- [ ] API hardening (auth, rate limits, OpenAPI) + deploy story + README

**Artifact gate:** deployable product with automated eval gates.

---

## Concept ↔ phase map (for reference)

| Original module | Phase |
| --- | --- |
| M1 LLMs from a builder's view | 1 |
| M2 Data parsing & structures | 1 |
| M3 Embeddings & vector search | 1 + 3 |
| M4 RAG end-to-end | 1 + 2 |
| M5 Agents & production | 4 + 5 + 6 |
| M5b n8n | 6 |
| Capstone | Veritas itself |
