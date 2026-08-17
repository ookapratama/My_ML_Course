# Product Plan: Veritas — A Trustworthy RAG Engine

> Working name: **Veritas** (Latin: *truth*). Change freely.
> A standalone, portfolio-grade product. No client/company affiliation.
> Thesis: most RAG demos retrieve and generate. Almost none can **prove** they
> are correct, **show** what happened, or **fix** themselves. Veritas does all three.

---

## 1. The one-sentence pitch

**Veritas is a RAG engine that ships with its own evaluation harness, full request
tracing, and a self-correcting retrieval loop — so every answer is measurable,
observable, and grounded.**

This is the gap MAANG-tier / frontier teams hire for: not "can you call an LLM,"
but "can you build the infrastructure that makes LLM systems *trustworthy in
production*."

---

## 2. Why this product (the career thesis)

| Most portfolios | Veritas |
| --- | --- |
| `.similarity_search()` → prompt → answer | Hybrid retrieval + reranking, benchmarked with recall@k / nDCG |
| "It works on my example" | A golden eval set + faithfulness/correctness scores per change |
| No idea why an answer was wrong | Full trace: query → retrieved chunks → prompt → tokens → cost → latency |
| Breaks on hard questions | Agent grades its own context, re-queries, and refuses when unsure |

The differentiator is **evaluation + observability**. Building those forces you to
build everything else correctly, and almost no junior portfolio has them.

---

## 3. Architecture (target end-state)

```
                          ┌─────────────────────────────────────────┐
                          │              Veritas API (FastAPI)        │
                          │   /ingest   /query   /eval   /traces      │
                          └───────────────┬───────────────────────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────────────┐
        │                                 │                                 │
        ▼                                 ▼                                 ▼
┌───────────────┐               ┌───────────────────┐             ┌───────────────────┐
│  Ingestion    │               │  Retrieval        │             │  Generation       │
│  - parse      │               │  - BM25 (sparse)  │             │  - prompt assembly│
│  - chunk      │               │  - dense (vector) │             │  - Claude / Ollama│
│  - embed      │──pgvector────▶│  - RRF fusion     │────────────▶│  - streamed parse │
│  - index      │               │  - cross-encoder  │             │  - citations      │
└───────────────┘               │    rerank         │             └─────────┬─────────┘
                                └───────────────────┘                       │
                                          ▲                                 │
                                          │  re-query if context weak       │
                                ┌─────────┴──────────┐                      │
                                │  Agentic loop      │◀─────────────────────┘
                                │  - grade context   │   grade answer
                                │  - decompose query │
                                │  - decide / refuse │
                                └────────────────────┘

   Cross-cutting (instrument everything):
   ┌────────────────────────┐      ┌────────────────────────┐
   │  Observability          │      │  Evaluation harness     │
   │  - trace store (Postgres)│      │  - golden dataset       │
   │  - per-call spans        │      │  - retrieval metrics    │
   │  - latency / cost / tokens│     │  - generation metrics   │
   │  - dashboard (Vite)      │      │  - regression on CI     │
   └────────────────────────┘      └────────────────────────┘

   Automation layer:  n8n (self-hosted) — ingestion triggers, nightly eval runs,
                      regression alerts (Slack/email), webhook entrypoints.
```

---

## 4. Tech stack

- **Core / ML:** Python + `uv`. FastAPI for the API.
- **Retrieval:** Postgres + `pgvector` (dense) + Postgres full-text or `bm25` for sparse;
  cross-encoder reranker via Hugging Face (`sentence-transformers`).
- **Embeddings:** start with a hosted/open embedding model; keep it swappable behind an interface.
- **LLM access:** Claude API (Sonnet for generation, Haiku for cheap grading/judging); Ollama for free local iteration.
- **Eval:** hand-built core metrics; LLM-as-judge via Claude. RAGAS as a reference, not a crutch.
- **Observability:** minimal trace store in Postgres first (to *understand* it), then align to
  OpenTelemetry GenAI semantic conventions for industry credibility.
- **Automation:** n8n, self-hosted via Docker Compose alongside Postgres.
- **Dashboard:** small React + Vite app (traces + eval results). Streamlit allowed for a faster v0.
- **App glue (optional):** Hono.js / Node where TS fits better than Python.

---

## 5. The hand-code core (calculator-forbidden)

Build these by hand once — they are the intuition the whole product rests on:

1. Prompt construction + streaming response parse.
2. Chunking + cosine similarity, computed manually once.
3. The retrieve → augment → generate loop.
4. RRF fusion (combine BM25 + dense rankings by hand).
5. One retrieval metric (recall@k or nDCG) and one generation metric (faithfulness) from scratch.
6. The agent loop: grade context → decide re-query / answer / refuse.
7. A single end-to-end trace span, written to the store by hand.

Everything else (boilerplate, config, UI, types, scaffolding) → delegate to AI.

---

## 6. Phased roadmap (incremental — each phase ships something demoable)

> Pace assumption: <5 hrs/week. Estimates are honest, not optimistic.
> Rule: **never** start a phase before the previous phase's artifact runs and is measured.

### Phase 0 — Foundations & scaffolding · ~1 week
- Repo structure, `uv` env, Docker Compose (Postgres + pgvector + n8n).
- Swappable interfaces: `Embedder`, `LLMClient`, `Retriever`, `Tracer`.
- **Ships:** `docker compose up` brings the whole local stack online.

### Phase 1 — Baseline RAG · ~3 weeks
- Ingestion (parse → chunk → embed → index) + naive dense retrieval + generation with citations.
- Intentionally simple — this is the skeleton everything else attaches to and improves on.
- **Ships:** ask a question over a real document corpus, get a cited answer.

### Phase 2 — Evaluation harness (the differentiator) · ~4 weeks
- Build a golden dataset (questions + ground-truth answers + relevant chunk labels).
- Retrieval metrics: recall@k, precision@k, MRR, nDCG.
- Generation metrics: faithfulness (groundedness), answer relevance, correctness vs golden, citation accuracy.
- LLM-as-judge (Claude Haiku) for the subjective metrics, with a heuristic baseline to validate the judge.
- **Ships:** `veritas eval` prints a scorecard for any config. Now every future change is measurable.

### Phase 3 — Hybrid retrieval + reranking · ~3–4 weeks
- Add BM25 (sparse) + RRF fusion + cross-encoder reranker.
- Prove each addition improves the Phase 2 scorecard (recall@k / nDCG before vs after).
- Tune chunk size, top-k, fusion weights — all decisions justified by metrics, not vibes.
- **Ships:** a benchmarked retrieval upgrade with a before/after table. This is the F-tier signal.

### Phase 4 — Observability & tracing · ~3 weeks
- Instrument every stage: span per query → retrieved chunks, scores, prompt, tokens, latency, cost.
- Trace store in Postgres; minimal dashboard (Vite) to inspect any past request.
- Align span schema to OpenTelemetry GenAI conventions.
- **Ships:** click any answer in the dashboard and see exactly why the system produced it.

### Phase 5 — Agentic self-correction · ~4 weeks
- Context grading: is the retrieved context sufficient? If not, decompose/re-query.
- Answer grading: is the draft grounded? If not, retry or **refuse** ("I don't have enough information").
- Loop termination + cost ceiling (no infinite agent loops).
- Measure: does the agentic loop beat baseline on the eval scorecard, and at what cost/latency?
- **Ships:** the system handles multi-hop and unanswerable questions honestly. This is the D-tier signal.

### Phase 6 — Productionization & automation · ~3–4 weeks
- n8n workflows: upload → trigger ingestion; nightly eval run → regression alert to Slack/email; webhook query entrypoint.
- API hardening: auth, rate limits, structured errors, OpenAPI docs.
- Deployment story (Docker Compose → optional single-VM deploy) + a README that reads like a real product.
- **Ships:** a deployable product with automated quality gates. Portfolio-complete.

**Total: ~5–7 months at <5 hrs/week.** Slower than a bootcamp; far deeper than one.

---

## 7. Mapping to the original module curriculum

The original `ai-engineering-learning-plan.md` modules are not discarded — they are the
*concepts*; Veritas phases are the *product* those concepts build toward.

| Original module | Lives in Veritas phase |
| --- | --- |
| M1 LLMs from a builder's view | Phase 1 (LLM client, prompting, streaming) |
| M2 Data parsing & structures | Phase 1 (ingestion pipeline) |
| M3 Embeddings & vector search | Phase 1 + 3 (dense + hybrid retrieval) |
| M4 RAG end-to-end | Phase 1–2 (RAG + eval) |
| M5 Agents & production | Phase 5–6 (agentic loop + productionization) |
| M5b n8n | Phase 6 (automation layer) |
| Capstone | Veritas itself |

---

## 8. What makes this defensible in an interview

For each phase you can answer the question that separates engineers from tutorial-followers:
- **"How do you know it's good?"** → the eval scorecard (Phase 2).
- **"Why did it give that answer?"** → the trace (Phase 4).
- **"What did you change and what did it buy you?"** → before/after metrics (Phase 3).
- **"What happens when it doesn't know?"** → it refuses, by design (Phase 5).
- **"How does it run in production?"** → automated eval gates + alerts (Phase 6).

---

## 9. Progress tracker

Progress is tracked in one place: **`PROGRESS.md`** (single source of truth — unifies
the learning lessons and the build artifacts per phase). Do not duplicate checkboxes here.

---

## 10. Open decisions (to settle before/at each phase)

- **Corpus:** what document set to demo on? (Pick a public, non-trivial, neutral domain — e.g. open
  technical docs, financial filings, or a research-paper set. Avoid anything proprietary.)
- **Golden dataset size:** start ~30–50 Q/A pairs; grow as needed for statistical signal.
- **Embedding model:** hosted vs open — decide in Phase 1, keep swappable.
- **Build vs adopt observability:** build minimal first; evaluate adopting OpenTelemetry/Langfuse later.

_Next step: Phase 0 — scaffold the repo and stand up the local stack._
