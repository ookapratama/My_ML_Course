# Python in 20 Hours — Pareto Track for AI Engineering

> Session 1–3 (selesai) + 7 Misi berbasis hasil (lihat bagian "Misi"). Tiap sesi belajar diakhiri **15-minute review**.
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

### [x] Session 2 — Core data structures
- [x] Lesson 1 — `list`, `dict`, `set`, `tuple`: when to use which; mutability rules; hashability — `fundamental/lesson_one` (folded into main.py notes)
- [x] Lesson 2 — Slicing (`a[1:5]`, `a[::-1]`), unpacking (`a, *rest = items`) — `fundamental/lesson_two/index.py`
- [x] Lesson 3 — **Comprehensions** — the #1 Python idiom (`[x*2 for x in xs if x > 0]` ≈ `xs.filter().map()`) — `fundamental/session_two/lesson_three/index.py`
- [x] Lesson 4 — Sorting with `key=` (≈ TS `sort(compareFn)` but by key extraction), `sorted` vs `.sort()` — `fundamental/session_two/lesson_four/index.py`
- **Resources:** [Official Tutorial ch. 5 (Data Structures)](https://docs.python.org/3/tutorial/datastructures.html), [Real Python: List Comprehensions](https://realpython.com/list-comprehension-python/)
- **15-min review** ✅ (do this after Lesson 4, once all sub-lessons are `[x]`)

### [x] Session 3 — Functions deep-dive
- [x] Lesson 1 — `*args` / `**kwargs`, keyword-only args (`def f(*, timeout=5)`) — `fundamental/session_three/lesson_one/index.py`
- [x] Lesson 2 — **The mutable-default-argument pitfall** (`def f(items=[])` — the classic bug) — `fundamental/session_three/lesson_two/index.py`
- [x] Lesson 3 — Closures and scope (`nonlocal`), lambdas (and why Python keeps them small) — `fundamental/session_three/lesson_three/index.py`
- [x] Lesson 4 — **Decorators** (≈ Express middleware / TS HOF) — write one by hand; `functools.wraps`, `functools.lru_cache` — `fundamental/session_three/lesson_four/index.py`
- **15-min review** ✅
- **Resources:** [Real Python: Primer on Decorators](https://realpython.com/primer-on-python-decorators/), [Real Python: *args and **kwargs](https://realpython.com/python-kwargs-and-args/)
- **15-min review** ✅ (do this after Lesson 4, once all sub-lessons are `[x]`)

> **Perubahan 2026-10-25:** Session 4–10 diganti 7 "Misi" kecil (alasan: bosan karena belajar tanpa tujuan terlihat). Isi Session 1–3 tidak berubah. Detail alasan: vault `Projects/ml-engineering-journey/Decisions/2026-10-25 - Kurikulum Python jadi misi berbasis hasil.md`. Backup versi lama: lihat riwayat git.

## Misi (menggantikan Session 4–10)

Aturan tiap misi:
- Ditulis satu kalimat tujuan di awal sesi: "Akhir sesi ini aku bisa melihat …".
- Konsep Python diajarkan **saat kode buntu**, dimulai dari hasil akhir lalu mundur ke konsep yang dibutuhkan.
- Kode ditulis user (guided mode). Hand-code tetap untuk chunking, cosine similarity, dan loop retrieve → augment → generate.
- Sesi 25 menit fokus + 5 menit jeda, maksimal 2 putaran. 15-minute review tetap di akhir tiap misi.
- Bosan lagi = sinyal untuk tinjau ulang urutan, bukan alasan berhenti.

**Skor pemahaman** (dicatat di vault `Learning/Python untuk AI Engineering/Reviews/`):
- Tiap sesi: 3 pertanyaan di akhir, skor `x/3`.
- Tiap misi (15-minute review): recall `x/5` (dari ingatan, sebelum buka catatan), micro-exercise (lulus di percobaan ke-berapa), dan satu tugas debug (kode rusak kecil: ketemu sebabnya, ya/tidak).
- Pembacaan: recall `<3/5` → topik goyah diulang di awal sesi berikutnya. `≥4/5` dua kali berturut-turut → misi berikutnya boleh dipercepat. Yang dinilai tren, bukan satu angka. Penilai awal adalah AI, jadi anggap angka sebagai indikasi.
- Data latihan: sintetis atau yang sudah disamarkan. Kunci API lewat env var, tidak pernah ditulis di kode.

### [ ] Misi 1 — Baca dan validasi data (lanjutan Session 4)
- [x] Lesson 1 — **Class dan object**: `class`, instance, attribute, `__init__`, `self` — `fundamental/session_four/lesson_one/index.py`
- [x] Lesson 2 — **Method dan dunder methods**: `__repr__`, `__eq__`, `__len__` — `fundamental/session_four/lesson_two/index.py`
- [x] Lesson 3 — **`@dataclass`** (sedang berjalan) — `fundamental/session_four/lesson_three/index.py`
- [ ] Lesson 4 — **Pydantic v2 models**: validasi + serialisasi (≈ Zod) — `fundamental/session_four/lesson_four/index.py`
- [ ] Lesson 5 — **Baca CSV/JSON + `try/except`**: tolak baris rusak dengan pesan jelas — `fundamental/session_four/lesson_five/index.py`
- **Hasil yang terlihat:** skrip membaca file CSV/JSON sintetis, baris valid jadi model Pydantic, baris rusak dilaporkan dengan alasannya.
- **Resources:** [Real Python: Data Classes](https://realpython.com/python-data-classes/), [Pydantic docs — Models](https://docs.pydantic.dev/latest/concepts/models/)

### [ ] Misi 2 — Potong teks (chunking)
- Type hints dasar (`list[str]`, `| None`), fungsi murni, `pathlib.Path`, dasar `pytest` (1 happy path + 1 edge case)
- **Hand-code** fungsi `chunk_text` (edge case: teks kosong, hanya tanda baca, teks non-ASCII, pemisah berurutan)
- **Hasil yang terlihat:** satu dokumen terpotong jadi chunk rapi, tes lulus dengan `uv run pytest`.

### [ ] Misi 3 — Panggil LLM
- Panggilan API, env var (`os.environ`), `try/except/else/finally`, custom exception, context manager, `logging` dasar
- **Hasil yang terlihat:** kirim pertanyaan ke Claude/Ollama, jawaban tampil, error jaringan ditangani dengan pesan yang jelas.

### [ ] Misi 4 — Embedding dan cosine similarity
- List vs NumPy dasar (shape, dot product), `Protocol` untuk `Embedder` (≈ Go interface)
- **Hand-code** cosine similarity dengan shape comment `# (n, dim) @ (dim,) -> (n,)`
- **Hasil yang terlihat:** "cari kalimat paling mirip" dari 20 kalimat.

### [ ] Misi 5 — Mini-RAG
- Menyatukan Misi 1–4. **Hand-code** loop retrieve → augment → generate, hasil sebagai dataclass
- **Hasil yang terlihat:** tanya satu dokumen, dapat jawaban + sumber chunk. Ini pintu masuk ke Veritas Phase 1.

### [ ] Misi 6 — Banyak pertanyaan sekaligus (bonus)
- `asyncio`, `await`, `asyncio.gather`, semaphore untuk batas laju
- **Hasil yang terlihat:** 20 pertanyaan jalan bersamaan, lebih cepat dari berurutan.

### [ ] Misi 7 — Ukur kualitas (bonus)
- Generator dan `itertools.batched` (hanya yang dipakai), pandas dasar (`read_csv`, filter, `groupby`)
- **Hasil yang terlihat:** dari 10 pertanyaan uji, tampil berapa yang dijawab benar.

### Cadangan (dipelajari penuh hanya kalau penasaran atau dibutuhkan)
- `@property`, class vs instance attribute (sisa Session 4 Lesson 5 lama), kapan tidak memakai class
- Iterator protocol (`__iter__`/`__next__`), generator mendalam
- NumPy mendalam (broadcasting, boolean mask, `axis`)
- `TypeVar` dan generics

---

## Setelah misi

Kembali ke `PROGRESS.md` (di `ai-engineer/`) — Phase 0, tindakan berikutnya: scaffold repo + stand up local stack. Misi 1–5 sudah memberi mini-RAG yang bisa dipakai ulang di Phase 1.
