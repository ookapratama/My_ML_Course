# Roadmap Adjustment — DRAFT (2026-10-12, diperbarui 2026-10-17)

> Status: rancangan untuk dibahas. Belum final.
> Tidak mengubah `python-20h-plan.md`, `PROGRESS.md`, `product-plan.md`, atau `ai-engineering-learning-plan.md`.
> Model dan metode belajar dibahas terpisah setelah roadmap ini disetujui.

## Prinsip

1. **Satu tulang punggung belajar:** Python track (S4–S10) lalu Veritas. Tidak ada jalur belajar kedua.
2. **Data Engineering = lahan latihan dari pekerjaan** (`mch-airflow`), ditambah satu slot SQL kecil per minggu. Bukan jalur belajar tambahan.
3. **Pekerjaan menang atas belajar.** Minggu yang kosong karena kerja adalah data, bukan kegagalan.
4. **Veritas tidak dimulai sebelum Python track selesai** (aturan fase lama tetap berlaku).
5. **ambis-in adalah pekerjaan, bukan jalur belajar.** Ia boleh dipakai sebagai bahan banding konsep (RAG, eval), tapi tidak menambah kewajiban belajar.
6. Kemajuan dinilai dari: bisa menjelaskan, bisa menerapkan, bisa men-debug. Bukan dari jumlah jam.

## Kapasitas yang direncanakan

| Slot                       | Durasi               | Isi                                                                           |
| -------------------------- | -------------------- | ----------------------------------------------------------------------------- |
| Hari kerja, maks 3 malam   | 45–60 menit          | 1 sub-lesson Python, atau 1 slot SQL                                          |
| Akhir pekan, 1 blok        | 3–4 jam, dengan jeda | Latihan penghubung + review mingguan                                          |
| **Lantai (energi rendah)** | **15 menit**         | Recall 3 pertanyaan atau 1 latihan kecil. Tetap dihitung sebagai hari belajar |
| Libur                      | min. 1 hari/minggu   | Tanpa rasa bersalah                                                           |

Total rencana sekitar 7 jam/minggu. Kapasitas yang disebutkan lebih besar, dan sisanya adalah cadangan, bukan target.

## Tahapan (perkiraan, ditinjau ulang tiap 2 minggu)

| Tahap            | Perkiraan         | Python track                                           | SQL (lahan latihan: `mch-airflow`)                              | Hasil yang bisa ditunjukkan                                                                            |
| ---------------- | ----------------- | ------------------------------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| A. Eksperimen    | Minggu 1–2        | S4: class, dataclass, Pydantic                         | Blok 1: grain, fan-out, jenis join                              | Model Pydantic untuk baris CSV sintetis + catatan satu halaman: kenapa join `profile_summary` berisiko |
| B. Fondasi       | Minggu 3–6        | S5 (typing, error), S6 (generator), S7 (async)         | Blok 2: kunci unik, NULL, window, semantik upsert, rekonsiliasi | Skrip kecil mirip `compare_counts.py` untuk data sintetis                                              |
| C. Penutup track | Minggu 7–9        | S8 (NumPy), S9 (file, pandas), S10 (capstone mini-RAG) | Blok 3: waktu dan zona waktu, JSON/array, full vs incremental   | Mini-RAG yang jalan end-to-end                                                                         |
| D. Veritas       | Mulai setelah S10 | —                                                      | SQL dipakai langsung (pgvector, trace store)                    | Phase 0 lalu Phase 1 (cited answer), dengan gerbang artefak seperti di `product-plan.md`               |

Perkiraan waktunya jujur kasar. Kita koreksi di review minggu ke-2 berdasarkan kecepatan nyata.

## Target 31 Desember 2026

Dihitung dari 13 Oktober: sekitar 11 minggu, sekitar 77 jam. Kebutuhan sekitar 30 jam (Python S4–S10 sekitar 14 jam, SQL tiga blok sekitar 12–15 jam; angka SQL adalah perkiraan, belum teruji). Targetnya diukur dari **jumlah minggu efektif**, bukan dari tanggal.

| Level | Isi | Status |
|---|---|---|
| **Minimum (dijaga)** | Python S4–S7 selesai. SQL Blok 1–2 selesai. Review mingguan terisi | Komitmen |
| **Ideal (tantangan)** | Sampai S10 (mini-RAG). SQL Blok 3 | Hanya kalau minggunya lancar |
| **Bonus** | Veritas Phase 0 | Bukan target |
| **Di luar target** | Pindah karier | Dievaluasi Januari 2027, berdasarkan bukti kerja |

Perkiraan posisi per skenario (kasar):

| Skenario | Minggu efektif | Posisi 31 Desember |
|---|---|---|
| Lancar | sekitar 9 dari 11 | Python dan SQL selesai, Veritas Phase 0 selesai |
| Realistis | sekitar 6–7 | S7–S8, SQL Blok 1–2 (**sama dengan target minimum**) |
| Berat | sekitar 3–4 | S5–S6, SQL Blok 1 |

Aturan: kalau di titik tinjau posisimu di bawah skenario Berat, **turunkan target, bukan tambah jam**.

Titik tinjau: akhir Oktober (setelah Tahap A), pertengahan November, akhir November, pertengahan Desember.

Catatan karier: roadmap lama memperkirakan sekitar 7 bulan menuju portofolio RAG yang siap kerja pada 5 jam/minggu (sekitar Mei 2027). Itu perkiraan, bukan janji. Jalur yang disarankan: tumbuh dulu di posisi sekarang (pipeline dan `ambis-in` sudah menyentuh kedua bidang), kumpulkan bukti, lalu putuskan pindah dengan bukti di tangan.

## Kurikulum SQL (diurutkan menurut kemunculan di pekerjaanmu)

Latihan memakai data sintetis atau yang sudah disamarkan di Postgres lokal (`local-lab`), bukan production. Sebelum menjalankan query: tulis dulu prediksi hasilnya.

**Blok 1 — Dasar yang berulang**

- [ ] Grain: satu baris mewakili apa?
- [ ] Fan-out: join ke kunci tidak unik melipatgandakan baris (`SUM` jadi bengkak)
- [ ] `INNER` vs `LEFT JOIN`, dan anti-join (cari yang tidak punya pasangan)
- [ ] Urutan eksekusi: `WHERE` → `GROUP BY` → `HAVING`
- [ ] `UNION` vs `UNION ALL`

**Blok 2 — Kunci dan kualitas data**

- [ ] Kunci unik: `COUNT(*)` vs `COUNT(DISTINCT kunci)`
- [ ] NULL: `= NULL`, `NOT IN` vs `NOT EXISTS`, `COUNT(*)` vs `COUNT(kolom)`
- [ ] Window function: `ROW_NUMBER`, `LAG`, total kumulatif, ties (`RANK`/`DENSE_RANK`)
- [ ] Dedup: ambil baris terbaru per kunci
- [ ] Semantik upsert: `DO NOTHING` vs `DO UPDATE`, dan kenapa baris basi menumpuk
- [ ] Rekonsiliasi: bandingkan jumlah baris dan skema (`information_schema`)

**Blok 3 — Waktu, tipe, dan beban data**

- [ ] `DATE_TRUNC`, zona waktu (UTC vs WIB), dan mengisi minggu yang kosong (`generate_series`)
- [ ] Pembersihan tipe: `CAST`, lebar `varchar`, pembagian bilangan bulat (`100.0`)
- [ ] Kolom JSON dan array (`jsonb ->>`, `UNNEST`)
- [ ] Full load vs incremental, dan kenapa `updated_date` perlu diperiksa dulu
- [ ] Dasar `EXPLAIN` dan index

**Menyusul, bila perlu:** kohort, retensi, sesi (untuk dashboard Amplitude).

## Evaluasi mingguan (10 menit, akhir pekan)

1. Apa yang jalan, dan apa yang tidak?
2. Bagaimana energi minggu ini (1–5)?
3. Beban minggu depan: naik, tetap, atau turun?

Satu hal yang masih goyah dicatat dan diulang di awal sesi berikutnya.

Dicatat di vault: `Learning/Python untuk AI Engineering/Reviews/` (format `YYYY-Www`, minggu pertama 2026-W42). Status resmi Python track tetap di `python-20h-plan.md`; Overview di vault hanya snapshot.

## Sudah diputuskan (2026-10-17)

- Tahap A (minggu 1) dimulai **2026-10-17** (Sabtu).
- Catatan review mingguan disimpan di vault Obsidian (`Learning/`).
- Tracking S1–S3 sudah dicatat sebagai snapshot di Overview topik di vault.

## Belum diputuskan

- Metode dan model belajar (peran AI, urutan Tutor → Assessor → Reviewer, cara mengukur pemahaman).

## Glosarium (catatan istilah)

Ditambah setiap kali ada istilah baru.

**Pekerjaan data**
- **Data Engineering (DE)** — pekerjaan menyiapkan data: mengambil dari sumber, membersihkan, dan menyimpannya supaya siap dipakai (dashboard, laporan, model AI). Seperti dapur yang menyiapkan bahan sebelum dimasak.
- **Pipeline** — jalur otomatis yang memindahkan dan mengolah data dari satu tempat ke tempat lain.
- **Data warehouse (DWH)** — gudang data yang sudah dirapikan untuk dianalisis. Di pekerjaanmu: tier *bronze* (data mentah), *silver* (sudah digabung dan dibersihkan), *gold* (siap pakai, belum dibuat).
- **Airflow** — alat yang menjadwalkan dan menjalankan pipeline.
- **Full load / incremental** — full load: salin semua data tiap kali. Incremental: hanya salin yang baru atau berubah.
- **Rekonsiliasi** — mencocokkan dua sumber (misalnya production vs bronze) untuk membuktikan isinya sama.

**SQL**
- **Grain** — satu baris tabel mewakili apa (satu order? satu pembayaran? satu order × satu status?).
- **Fan-out** — baris berlipat ganda gara-gara join ke tabel yang kuncinya tidak unik, sehingga jumlah (`SUM`) jadi membengkak.
- **Join (`INNER` / `LEFT`)** — menggabungkan dua tabel. `INNER` hanya menyimpan yang punya pasangan; `LEFT` menyimpan semua baris kiri.
- **Anti-join** — mencari yang tidak punya pasangan (pelanggan yang belum pernah order).
- **Kunci unik** — kolom yang nilainya tidak boleh kembar, dipakai untuk mengenali satu baris.
- **NULL** — "tidak ada nilai". Bukan nol dan bukan teks kosong, dan perilakunya sering mengejutkan.
- **Window function** — menghitung sesuatu di antara baris-baris yang berdekatan tanpa menggabungkannya (peringkat, selisih dengan bulan lalu, total kumulatif).
- **Dedup** — membuang duplikat, biasanya menyisakan baris terbaru per kunci.
- **Upsert** — "insert kalau baru, update kalau sudah ada".
- **Zona waktu (UTC / WIB)** — acuan waktu. Data sering disimpan dalam UTC, sedangkan laporan dibaca dalam WIB (selisih 7 jam).
- **JSON / array** — kolom yang isinya berstruktur (objek atau daftar), bukan satu nilai sederhana.
- **EXPLAIN / index** — EXPLAIN menunjukkan cara database menjalankan query. Index membuat pencarian lebih cepat, seperti daftar isi buku.

**Python dan AI**
- **Pydantic / dataclass** — cara menulis class data yang rapi. Pydantic juga memeriksa isinya (≈ Zod di TypeScript).
- **Generator** — fungsi yang mengeluarkan data sedikit demi sedikit, hemat memori.
- **Async** — menjalankan banyak pekerjaan yang menunggu (misalnya panggilan API) secara bersamaan.
- **NumPy / pandas** — pustaka untuk menghitung angka dalam jumlah besar dan mengolah tabel.
- **AI Engineering** — membangun aplikasi dan sistem yang memakai model AI (bukan melatih model dari nol).
- **RAG** — AI menjawab dengan mencari potongan dokumen yang relevan dulu, lalu menjawab berdasarkan itu. **Mini-RAG** adalah versi kecil untuk latihan.
- **Veritas** — nama proyek portofolio RAG di roadmap ini: bisa dibuktikan benar (eval), dilacak (tracing), dan memperbaiki diri.
- **Eval (evaluation)** — mengukur kualitas jawaban dengan soal dan kunci jawaban, supaya perbaikan bisa dibuktikan.

**Python: class dan object**
- **Class** — cetakan. Mendefinisikan bentuk dan perilaku, belum berisi data milik siapa pun.
- **Object / instance** — hasil cetakan. `House("Jl. A")` membuat satu object.
- **Attribute** — data yang menempel pada object (`h.address`).
- **`__init__`** — method yang Python panggil otomatis tepat setelah object dibuat, untuk mengisinya (≈ constructor; lebih tepatnya *initializer*).
- **`self`** — object yang sedang diisi atau dipakai. Parameter pertama method, **dikirim Python otomatis**, tidak ditulis saat memanggil.
- **Class attribute vs instance attribute** — attribute di dalam class dipakai bersama. Python mencari ke object dulu, baru ke class-nya.
- **`TypeError`** — error karena pemakaian yang tidak sesuai, misalnya jumlah argumen tidak cocok dengan jumlah parameter.
- **Method** — function yang ditulis di dalam class. Parameter pertamanya `self`, dikirim Python otomatis.
- **Dunder method** — method berawalan dan berakhiran dua garis bawah (`__init__`). Tidak dipanggil sendiri; Python memanggilnya pada situasi tertentu.
- **`__repr__`** — menentukan tampilan object sebagai teks (`print(o)`, debugger). Harus `return` string, bukan `print`.
- **`__eq__`** — menentukan arti `==` untuk class. Bawaannya hanya menanyakan "object yang sama persis?".
- **`isinstance(x, Kelas)`** — `True` kalau `x` adalah object dari `Kelas`.
- **`NotImplemented`** — nilai khusus yang dikembalikan `__eq__` untuk berkata "saya tidak tahu cara membandingkan ini", agar Python mencoba sisi sebelahnya. Bukan `False`.
- **`__len__`** — membuat `len(object)` bisa dipakai. Harus mengembalikan bilangan bulat.
- **Unhashable** — object yang tidak bisa jadi key dictionary atau isi `set`. Terjadi kalau class mendefinisikan `__eq__` tanpa `__hash__`.
- **`AttributeError`** — error karena membaca attribute yang tidak ada pada object itu.

**Perencanaan**
- **Capstone** — proyek penutup yang menggabungkan semua yang sudah dipelajari.
- **Data sintetis** — data buatan yang bentuknya mirip aslinya, aman dipakai latihan.
- **Gerbang artefak** — aturan "fase berikutnya baru boleh dimulai kalau hasil fase ini jalan dan terukur".
- **Portofolio** — kumpulan bukti kerja yang bisa kamu tunjukkan ke orang lain.
- **Target minimum / ideal** — minimum: yang hampir pasti tercapai dan dijaga. Ideal: tantangan kalau minggu-minggunya lancar.
- **Cadangan (buffer)** — waktu kosong yang sengaja disisakan untuk minggu yang meleset.
