# Python in 20 Hours — Pareto Track for AI Engineering

> 10 sessions × 2 hours. Each session = **1h45m learn + practice** and a **15-minute review** at the end.
> Built for a developer who already knows Go / TypeScript / PHP — no "what is a variable" content.
> The 20% of Python that delivers 80% of what AI Engineering (and Veritas) needs.

## How to run a session

1. Start the session with `/learn-mode` and the session topic (e.g. `/learn-mode Session 3: functions deep-dive`).
2. Follow the Tutor → Assessor → Reviewer loop. A session only counts when the challenge passes (`[LESSON_PASSED]`).
3. Close with the **15-minute review** (protocol below), then tick the session's checkbox here.

## 15-minute review protocol (every session)

- **10 min — active recall:** answer 5 questions about today's material from memory, out loud or in writing, *before* checking notes.
- **4 min — micro-exercise:** re-write today's smallest core snippet from a blank file, no peeking.
- **1 min — log:** tick the checkbox below and note one thing that felt shaky (revisit it at the start of the next session).

---

## Sessions

### [x] Session 1 — Setup & syntax speedrun through a Go/TS lens
- `uv` install, `uv init`, `uv run`, how the venv works (≈ `node_modules` + `package.json`, but for the interpreter too)
- REPL workflow, `python -i`, f-strings, truthiness (`[]`, `{}`, `""`, `0`, `None` are falsy)
- Variables, `if/elif/else`, `for`/`while`, `range`, no braces — indentation is syntax
- Functions: `def`, default args, return values (tuples for multi-return, ≈ Go's `val, err`)
- **Resources:** [Official Python Tutorial ch. 3–5](https://docs.python.org/3/tutorial/), [uv docs](https://docs.astral.sh/uv/), [Learn X in Y Minutes: Python](https://learnxinyminutes.com/docs/python/)
- **15-min review** ✅

### [ ] Session 2 — Core data structures
- [x] Lesson 1 — `list`, `dict`, `set`, `tuple`: when to use which; mutability rules; hashability — `fundamental/lesson_one` (folded into main.py notes)
- [x] Lesson 2 — Slicing (`a[1:5]`, `a[::-1]`), unpacking (`a, *rest = items`) — `fundamental/lesson_two/index.py`
- [x] Lesson 3 — **Comprehensions** — the #1 Python idiom (`[x*2 for x in xs if x > 0]` ≈ `xs.filter().map()`) — `fundamental/session_two/lesson_three/index.py`
- [ ] Lesson 4 — Sorting with `key=` (≈ TS `sort(compareFn)` but by key extraction), `sorted` vs `.sort()` — `fundamental/lesson_four/index.py`
- **Resources:** [Official Tutorial ch. 5 (Data Structures)](https://docs.python.org/3/tutorial/datastructures.html), [Real Python: List Comprehensions](https://realpython.com/list-comprehension-python/)
- **15-min review** ✅ (do this after Lesson 4, once all sub-lessons are `[x]`)

### [ ] Session 3 — Functions deep-dive
- `*args` / `**kwargs`, keyword-only args (`def f(*, timeout=5)`)
- **The mutable-default-argument pitfall** (`def f(items=[])` — the classic bug)
- Closures and scope (`nonlocal`), lambdas (and why Python keeps them small)
- **Decorators** (≈ Express middleware / TS HOF) — write one by hand; `functools.wraps`, `functools.lru_cache`
- **Resources:** [Real Python: Primer on Decorators](https://realpython.com/primer-on-python-decorators/), [Real Python: *args and **kwargs](https://realpython.com/python-kwargs-and-args/)
- **15-min review** ✅

### [ ] Session 4 — OOP the Python way
- Classes, `__init__`, `self` (explicit, unlike `this`), dunder methods (`__repr__`, `__eq__`, `__len__`)
- `@dataclass` — 90% of your classes should be this or Pydantic
- **Pydantic v2 models** — validation + serialization (≈ Zod); this is the backbone of FastAPI and Veritas' typed interfaces
- `@property`, class vs instance attributes; when NOT to use classes (modules + functions are fine)
- **Resources:** [Real Python: Data Classes](https://realpython.com/python-data-classes/), [Pydantic docs — Models](https://docs.pydantic.dev/latest/concepts/models/)
- **15-min review** ✅

### [ ] Session 5 — Typing, errors, context managers
- Type hints: `list[str]`, `dict[str, int]`, `Optional`/`| None`, `TypeVar`, generics
- **`Protocol`** — structural typing ≈ Go interfaces; exactly how Veritas' swappable `Embedder` / `LLMClient` / `Retriever` interfaces will be defined
- Exceptions & EAFP ("ask forgiveness, not permission" — vs Go's explicit `err` checks); `try/except/else/finally`, custom exceptions
- Context managers: `with open(...)`, writing your own via `contextlib.contextmanager` (≈ Go's `defer`)
- **Resources:** [mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html), [Real Python: Python Type Checking](https://realpython.com/python-type-checking/)
- **15-min review** ✅

### [ ] Session 6 — Iterators & generators
- The iteration protocol (`__iter__` / `__next__`) — why `for` works on everything
- **`yield`** and generator functions — lazy, memory-efficient pipelines
- Generator expressions vs list comprehensions (when to stream vs materialize)
- `itertools` greatest hits: `chain`, `islice`, `batched` — this maps directly to document chunking and streaming LLM responses
- **Resources:** [Real Python: Generators](https://realpython.com/introduction-to-python-generators/), [itertools docs](https://docs.python.org/3/library/itertools.html)
- **15-min review** ✅

### [ ] Session 7 — Async Python
- `asyncio` event loop vs Node's (explicit `asyncio.run`, nothing is async by default)
- `async def` / `await`, `asyncio.gather` (≈ `Promise.all`), `asyncio.TaskGroup`
- `httpx` async client — concurrent HTTP calls
- **Semaphore-based rate limiting** — the exact pattern for firing concurrent LLM API calls without hitting rate limits
- **Resources:** [Real Python: Async IO in Python](https://realpython.com/async-io-python/), [httpx docs — Async](https://www.python-httpx.org/async/)
- **15-min review** ✅

### [ ] Session 8 — NumPy essentials
- `ndarray`: shape, dtype, why it's 100× faster than lists (vectorization)
- Indexing, boolean masks, `axis` semantics
- **Broadcasting** — the one concept that unlocks all of NumPy/PyTorch
- Dot product → **hand-code cosine similarity** with shape comments `# (n, dim) @ (dim,) -> (n,)` — this directly pre-loads a Veritas Phase 1 hand-code item
- **Resources:** [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html), [NumPy: Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- **15-min review** ✅

### [ ] Session 9 — Files, data handling, pandas basics
- `pathlib.Path` (never string paths), reading/writing text and binary
- `json` module, `csv` module — parsing real formats (feeds Veritas ingestion)
- Env vars (`os.environ`, `python-dotenv`), `logging` basics (not `print`)
- pandas in 30 minutes: `DataFrame`, `read_csv`, filtering, `groupby` — just the data-engineering slice
- **Resources:** [pandas: 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html), [Real Python: pathlib](https://realpython.com/python-pathlib/)
- **15-min review** ✅

### [ ] Session 10 — Capstone + testing
- **Mini-RAG warm-up, end to end:** read a text file → chunk it (generator from S6) → toy-embed each chunk (NumPy from S8) → cosine-rank against a query → print top-k with a `dataclass` result type (S4) and `Protocol`-based embedder (S5)
- `pytest` basics: co-located `test_*.py`, happy path + 1 edge case per function, `uv run pytest`
- Project layout under `uv`: `pyproject.toml`, entry point, `uv run`
- **This is the on-ramp to Veritas Phase 1** — the next session after this one is Veritas, not more Python
- **Resources:** [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html), your own Sessions 1–9 notes
- **15-min review** ✅ (extended: review the shakiest topic from the whole track)

---

## After the track

Return to `D:\ooka\dev\ai-engineer\PROGRESS.md` — Phase 0, next action: scaffold repo + stand up the local stack. Everything hand-coded here (chunking, cosine similarity, typed interfaces) gets reused there for real.
