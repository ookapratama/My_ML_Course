# Learning Plan: Career Switch → LLM/RAG App Engineer

> Personal roadmap for transitioning into AI Engineering while running ADHARA.
> Pace: **< 5 hrs/week** · Style: **hybrid coding** · Math: **light, just-in-time**.

---

## 1. Context

You are a technical CEO (ADHARA / Pelindo SCP) already fluent in Go, Node, React, and
TypeScript, transitioning into AI Engineering. This plan answers: a detailed roadmap,
pros/cons, decision space, the _"do I still need to hand-code?"_ question, and how to choose
the right system architecture.

| Dimension    | Your answer              | Effect on the plan                                               |
| ------------ | ------------------------ | ---------------------------------------------------------------- |
| Target role  | **LLM/RAG App Engineer** | Software-engineering–heavy, math-light. Plays to your strengths. |
| Time budget  | **< 5 hrs/week**         | Lean, project-driven. ~7 month sustainable horizon.              |
| Coding style | **Hybrid**               | Hand-code core concepts; AI for boilerplate/glue.                |
| Math level   | **Light / rusty**        | Just-in-time, intuition-first math. No proofs.                   |

The good news: **LLM/RAG app engineering is ~80% software engineering you already know**
(APIs, data plumbing, services, state) and ~20% new ML concepts. You are extending the career
you have, not restarting.

---

## 2. Strategic answer: do you still need to code manually?

**Yes — but selectively. This is the whole point of the "Hybrid" choice.**

Analogy: AI assistants are like a calculator for a maths student. A calculator is fine _after_
you understand arithmetic — harmful _before_, because you never build number sense. Same here:
hand-code the handful of concepts that form your intuition, then let AI handle the repetitive
scaffolding forever after.

**Hand-code these (the "calculator-forbidden" core — ~5 things total):**

- Building a prompt + parsing a streamed LLM response
- Chunking a document + computing cosine similarity _once_ by hand
- The retrieve → augment → generate loop of RAG
- A tool/function-call schema + a minimal agent loop
- One evaluation harness (does my RAG answer correctly?)

**Let AI write (forever):** boilerplate, config, glue code, UI, types, test scaffolding.

Rationale: with <5 hrs/week, typing boilerplate is waste. Spend that time on the concepts you
must _feel_ to design systems well. After that, AI-assisted is correct and efficient.

---

## 3. Curriculum (5 bite-sized modules)

Each module = ~3–4 weeks at your pace, ends in a small shippable artifact. Taught as:
analogy → core idea → how it works → minimal hand-coded example → common pitfalls
(the `/learn-mode` loop: Tutor → Assessor → Reviewer per lesson).

**Prerequisites (already have):** Python comfort, HTTP/REST, git. No gap to close.

### Module 1 — LLMs from a builder's view

- **Concepts:** tokens, context window, temperature/top-p, embeddings (intro), prompting patterns.
- **You build:** a typed LLM client wrapper (mirrors your `lib/axios.ts` mental model).
- **Hand-code:** prompt construction + streaming response parse.
- **Math:** none beyond "an embedding is a list of numbers."
- **Goal:** call an LLM correctly, control its output, understand cost/latency drivers.

### Module 2 — Data parsing & data structures (the foundation)

- **Concepts:** parsing real-world data (JSON, CSV, HTML, PDF, plain text); the data structures
  that underpin everything — arrays/lists (an embedding _is_ an array of floats), dictionaries/
  hash maps (the index lookup), trees & graphs (how vector indexes like HNSW organize data),
  and why structure dictates speed (Big-O intuition, no heavy theory).
- **You build:** a document-ingestion pipeline — read messy files → clean → normalize into a
  consistent structured shape ready for chunking.
- **Hand-code:** a parser for each format (parse JSON/CSV by hand once; walk an HTML/PDF tree);
  implement a hash-map lookup and a simple tree traversal yourself to _feel_ the structures.
- **Math:** none — pure data/structures intuition.
- **Goal:** confidently turn any messy real-world data into clean, structured input — and
  understand _why_ the right data structure makes retrieval fast. Feeds Module 3.

### Module 3 — Embeddings & vector search (the heart of RAG)

- **Concepts:** what an embedding _is_, vector databases, similarity search, chunking.
- **You build:** semantic search over a folder of docs.
- **Hand-code:** chunk text + compute cosine similarity by hand _once_, then switch to a vector DB.
- **Math:** vectors, dot product, cosine similarity (intuition-first, ~30 min).
- **Goal:** understand _why_ retrieval works, not just call a library.

### Module 4 — RAG pipeline end-to-end

- **Concepts:** retrieve → augment → generate, chunking strategies, citations, hallucination, eval.
- **You build:** a working RAG Q&A bot over real ADHARA / port-ops docs.
- **Hand-code:** the retrieval + prompt-assembly loop; a tiny eval harness.
- **Goal:** ship a RAG system you could actually demo to your team.

### Module 5 — Agents, tool-calling & production concerns

- **Concepts:** function/tool calling, agent loops, guardrails, evaluation, caching, observability, cost.
- **You build:** an agent that calls a real tool (e.g., the SCP container-tracking API).
- **Hand-code:** the tool schema + the agent loop.
- **Goal:** design and reason about production AI features end-to-end.

**Capstone (high-motivation):** an internal ADHARA assistant — RAG over port-service docs + a
tool that hits container tracking. Real, useful, portfolio-worthy.

---

## 4. System architecture: your decision space

Because Pelindo is a state-owned port operator, **Indonesian data-sovereignty / residency is a
real constraint** — it pushes toward self-hostable storage.

| Option                       | Stack                                                                                         | Pros                                                                                       | Cons                                                                                                       |
| ---------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **A — Fully managed**        | Hosted vector DB (Pinecone) + frontier LLM API + LangChain/LlamaIndex                         | Fastest to learn & ship, minimal ops                                                       | Data leaves your control, recurring cost, lock-in. Weak fit for port data                                  |
| **B — Fully self-hosted**    | `pgvector` on your Postgres + open models (Ollama/vLLM) + custom orchestration                | Full data control, residency-friendly, reuses your stack, no per-token cost                | More ops, open models lag frontier quality, you maintain everything                                        |
| **C — Hybrid (recommended)** | `pgvector` storage/retrieval + frontier LLM (Claude/GPT) via API + thin Node/Go orchestration | Best answer quality, your data stays in _your_ Postgres, pragmatic ops, reuses your skills | Generation calls hit external API — mitigate with PII redaction + self-hosted fallback for sensitive paths |

**Recommendation: learn on Option A (fastest feedback), build the capstone on Option C.**

---

## 5. Tooling stack (close to what you know)

- **Language:** Python for ML/RAG core (industry standard); keep TypeScript/Node for the app layer.
- **Frameworks:** Hugging Face + LangChain/LlamaIndex.
- **Vector store:** `pgvector` (extends your Postgres — no new infra to learn).
- **LLM access:** frontier API for quality; Ollama locally for free experimentation.
- **Env:** your existing Arch + Neovim + Python venv. No new editor.

---

## 6. Realistic timeline (< 5 hrs/week)

| Phase    | Duration   | Outcome                                              |
| -------- | ---------- | ---------------------------------------------------- |
| Module 1 | ~1 month   | Confident LLM API usage                              |
| Module 2 | ~1 month   | Document-ingestion pipeline + data-structure fluency |
| Module 3 | ~1 month   | Working semantic search                              |
| Module 4 | ~1.5 month | Shippable RAG Q&A bot                                |
| Module 5 | ~1.5 month | Tool-using agent                                     |
| Capstone | ~1 month   | ADHARA internal assistant (portfolio piece)          |

**~7 months to a job-ready RAG portfolio.** Slower than a bootcamp, but sustainable while
running a company — and the capstone doubles as real business value.

---

## 7. Pros / cons of this approach

**Pros:** leverages existing skills (fast ROI), low math burden, project-driven (motivating),
capstone delivers real ADHARA value, hybrid coding keeps fundamentals without wasting scarce time.

**Cons:** <5 hrs/week makes it slow; risk of stalling if business gets busy (mitigate: tiny weekly
goals, ship something every module); LLM/RAG depth ≠ deep ML theory (acceptable — not your target).

---

## 8. How we'll run it (execution mode)

Per lesson, the `/learn-mode` loop:

1. **Tutor** — teaches one lesson: analogy → core concept → how it works → hand-coded example → pitfalls.
2. **Assessor** — gives a short challenge (concept Q, tiny code task, or spot-the-bug). _Pause for your answer._
3. **Reviewer** — checks your answer; hints if off, confirms + `[LESSON_PASSED]` if right, then next lesson.

---

## 9. Verification (how you'll know it's working)

- End of each module: a running artifact you can demo (search tool, RAG bot, agent).
- Each lesson gated by passing the Assessor challenge — no moving on without demonstrated understanding.
- Capstone = the real test: a working, useful AI feature you built and can explain end-to-end.

---

## 10. Progress tracker

Progress now lives in **`PROGRESS.md`** (single source of truth). The modules below are the
*concepts*; they are mapped onto the product phases of **`product-plan.md`** (product: **Veritas**,
a trustworthy RAG engine — standalone, not ADHARA-specific). When a lesson passes, tick it in
`PROGRESS.md`, not here. See the concept ↔ phase map at the bottom of `PROGRESS.md`.

---

_Next step: begin Module 1, Lesson 1 (LLMs from a builder's view) via the Tutor loop._
