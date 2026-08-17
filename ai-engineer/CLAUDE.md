# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

Standalone, portfolio-grade product — **not** affiliated with any company or client. The goal is a product that reads as MAANG-tier / frontier-AI-team credible.

**Product: Veritas** — a trustworthy RAG engine that ships with its own evaluation harness, full request tracing, and a self-correcting retrieval loop. Thesis: most RAG demos retrieve and generate; Veritas can *prove* it's correct (eval), *show* what happened (observability), and *fix itself* (agentic loop).

Source of truth for scope and roadmap: **`product-plan.md`**.
Conceptual background curriculum: `ai-engineering-learning-plan.md` (concepts feed the product; the ADHARA framing there is superseded — the product is standalone).

## Learning loop

The user is learning while building. Default to the `/learn-mode` pattern — **Tutor → Assessor → Reviewer**:
1. Teach one concept: analogy → core idea → how it works → hand-coded example → pitfalls.
2. Give a short challenge. Pause for the user's answer.
3. Check, hint if off, confirm + `[LESSON_PASSED]` if right, then next.

Never advance without a passed Assessor challenge.

## Progress & sync protocol (important)

`PROGRESS.md` is the **single source of truth** for progress — it unifies learning (lessons) and
building (phase artifacts) per phase. `product-plan.md` and `ai-engineering-learning-plan.md` both
point to it and hold no checkboxes of their own.

- When a lesson passes (`[LESSON_PASSED]`) → tick its **Learn** box in `PROGRESS.md`.
- When a phase artifact runs and is measured → tick its **Build** box in `PROGRESS.md`.
- At the end of every session → update the **Current position** block (Phase / Lesson / Next action) at the top of `PROGRESS.md`.
- Never record progress in the two plan files; they are read-only for status.

## What to hand-code vs delegate

**Hand-code always (calculator-forbidden core):**
- Prompt construction + streaming response parse
- Chunking + cosine similarity (once, manually)
- The retrieve → augment → generate loop
- RRF fusion (combine BM25 + dense rankings)
- One retrieval metric (recall@k / nDCG) + one generation metric (faithfulness), from scratch
- The agent loop: grade context → re-query / answer / refuse
- One end-to-end trace span written by hand

**Delegate to AI:** boilerplate, config, UI, types, test scaffolding.

## Roadmap (phases — see `product-plan.md` for detail)

| Phase | Focus | Ships |
|-------|-------|-------|
| 0 | Foundations & scaffolding | `docker compose up` local stack |
| 1 | Baseline RAG | cited answer over a real corpus |
| 2 | Evaluation harness *(differentiator)* | `veritas eval` scorecard |
| 3 | Hybrid retrieval + reranking | benchmarked before/after table |
| 4 | Observability & tracing | dashboard showing why an answer happened |
| 5 | Agentic self-correction | honest handling of hard/unanswerable questions |
| 6 | Productionization & n8n automation | deployable product + automated eval gates |

Rule: never start a phase before the previous phase's artifact runs **and is measured**.

## Stack conventions

- **Core / ML:** Python + `uv`. FastAPI for the API. PyTorch / Hugging Face / LangChain where they fit.
- **Retrieval:** Postgres + `pgvector` (dense) + BM25 (sparse) + cross-encoder reranker.
- **LLM access:** Claude API (Sonnet = generation, Haiku = grading/judging); Ollama for local iteration.
- **Eval:** hand-built core metrics + LLM-as-judge (Claude). RAGAS as reference only.
- **Observability:** minimal Postgres trace store first; align to OpenTelemetry GenAI conventions.
- **Automation:** n8n, self-hosted via Docker Compose.
- **Dashboard:** React + Vite (Streamlit allowed for a fast v0).
- **Package managers:** `uv` (Python), `pnpm` (Node).

## ML code conventions

- Always include tensor/array shape annotations in comments, e.g. `# (batch, seq_len, hidden)`.
- Keep models/embedders/retrievers behind swappable interfaces (`Embedder`, `LLMClient`, `Retriever`, `Tracer`).
- Every retrieval/generation change must be justified by an eval-scorecard delta, not intuition.

## Project structure (to be built)

```
ai-engineer/
├── product-plan.md                   # product roadmap — source of truth
├── ai-engineering-learning-plan.md   # background concept curriculum
├── CLAUDE.md
├── docker-compose.yml                # Postgres + pgvector + n8n
├── veritas/                          # Python package (FastAPI app + core)
│   ├── ingestion/                    # parse → chunk → embed → index
│   ├── retrieval/                    # dense, sparse, fusion, rerank
│   ├── generation/                   # prompt assembly, LLM, citations
│   ├── agent/                        # context/answer grading, re-query loop
│   ├── eval/                         # golden set, metrics, judge, scorecard
│   └── observability/                # trace store, spans
├── dashboard/                        # React + Vite (traces + eval results)
└── workflows/                        # n8n workflow JSON exports
```

## Running (target commands)

```bash
docker compose up -d        # Postgres + pgvector + n8n
uv run uvicorn veritas.api:app --reload   # API
uv run veritas eval         # run the eval scorecard
pnpm --dir dashboard dev    # dashboard
```

## Progress

`PROGRESS.md` (single source of truth). See the sync protocol above.
