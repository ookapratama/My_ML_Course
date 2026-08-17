# AI Engineer — Veritas

Active project: a standalone, portfolio-grade trustworthy-RAG product — not affiliated with any company or client.

## Product: Veritas

A RAG engine that ships with its own evaluation harness, full request tracing, and a self-correcting retrieval loop. Thesis: most RAG demos just retrieve and generate; Veritas can *prove* it's correct (eval), *show* what happened (observability), and *fix itself* (agentic loop).

- Source of truth for scope/roadmap: [`product-plan.md`](./product-plan.md)
- Conceptual background curriculum: [`ai-engineering-learning-plan.md`](./ai-engineering-learning-plan.md)
- **Progress (single source of truth):** [`PROGRESS.md`](./PROGRESS.md)

## Python fundamentals fast-track

[`fundamental/`](./fundamental) — a 20-hour Pareto curriculum covering the Python needed for AI engineering (data structures, functions, OOP, typing/errors, generators, async, NumPy, pandas), taught through a Go/TypeScript lens since that's the user's existing background. Curriculum + progress tracker: [`fundamental/python-20h-plan.md`](./fundamental/python-20h-plan.md).

## Roadmap

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

## Stack

Python + `uv`, FastAPI, Postgres + `pgvector` (dense) + BM25 (sparse) + cross-encoder reranker, Claude API (Sonnet = generation, Haiku = judging) + Ollama for local iteration, n8n (self-hosted, Docker Compose), React + Vite dashboard.

See [`CLAUDE.md`](./CLAUDE.md) for full conventions.
