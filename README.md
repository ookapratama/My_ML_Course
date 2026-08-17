# ML Engineering Journey

A record of my path from software engineering into ML/AI engineering — coursework fundamentals through to a portfolio-grade, production-style project.

## Structure

```
ml-engineering-journey/
├── My_ML_Course/     # ML fundamentals coursework: preprocessing, regression models, hackathon exercises
└── ai-engineer/       # Active project: Veritas — a trustworthy RAG engine (eval harness, tracing, self-correction)
```

### [`My_ML_Course/`](./My_ML_Course)

Early ML coursework — data preprocessing, regression techniques (simple/multiple/polynomial/decision-tree/random-forest/SVR), and hackathon exercises. Mostly Jupyter notebooks working through core scikit-learn concepts.

### [`ai-engineer/`](./ai-engineer)

The active, portfolio-grade project. Two tracks running in parallel:

- **Python fundamentals fast-track** (`ai-engineer/fundamental/`) — a 20-hour Pareto curriculum covering the Python needed for AI engineering, taught through a Go/TypeScript lens.
- **Veritas** (`ai-engineer/product-plan.md`) — a trustworthy RAG engine that ships with its own evaluation harness, full request tracing, and a self-correcting retrieval loop. See `ai-engineer/PROGRESS.md` for current phase/status.

## Why this repo exists

Most ML learning repos are a pile of notebooks. This one is meant to show progression: from coursework fundamentals to a hand-coded, evaluated, observable RAG system — with the reasoning and the metrics to back it up, not just a demo.
