# Learn Mode: Python for AI Engineering

## Goal
- Learning Python fundamentals fast (20-hour Pareto track) to unblock the Veritas RAG project
- Compare patterns to my existing knowledge (Go, TypeScript/Node.js, PHP, React)
- Curriculum + progress tracker: `python-20h-plan.md` in this directory

## Stack Details
- Language: Python 3.12+
- Framework: none (Pydantic v2 and FastAPI concepts touched where relevant to Veritas)
- Package manager: `uv`

## Learning Rules
- Explain new concepts with analogies to Go / TypeScript first, e.g.:
  - `Protocol` ≈ Go interface (structural typing)
  - `asyncio` event loop ≈ Node.js event loop (but explicit, opt-in)
  - decorator ≈ TS higher-order function / Express middleware
  - `**kwargs` ≈ TS object spread into named options
  - list comprehension ≈ `array.map().filter()` chain
- Always show the equivalent pattern in Go or TypeScript when applicable
- Break down unfamiliar paradigms step-by-step (duck typing, EAFP, comprehensions, generators)
- Treat compiler/runtime errors (tracebacks) as learning moments — read them bottom-up together
- Follow the `/learn-mode` loop: Tutor → Assessor → Reviewer. Never advance a session without a passed challenge (`[LESSON_PASSED]`)
- Sessions with multiple lessons (e.g. Session 2) are tracked as sub-checkboxes under the session's main checkbox in `python-20h-plan.md` — tick each lesson's `[x]` as it passes; tick the session's own checkbox only once every lesson under it is done
- When a lesson/session passes, tick its checkbox in `python-20h-plan.md` (progress lives there, not in the parent `PROGRESS.md`)
- Practice code for each lesson lives in its own folder: `fundamental/lesson_<n>/index.py` (e.g. `fundamental/lesson_two/index.py`) — keep exercise code there instead of `main.py`, one folder per lesson

## Project Conventions
- Follow the naming and code style from global CLAUDE.md, but adapt to Python idioms when they conflict:
  - `snake_case` for variables and functions (not camelCase)
  - `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants
  - Files: `snake_case.py` (not kebab-case — hyphens break imports)
  - Type hints everywhere; early returns; max ~40 lines per function
  - Tests: `test_<name>.py` co-located with source, run with `pytest`
- ML/array code: always include shape annotations in comments, e.g. `# (n, dim)`
