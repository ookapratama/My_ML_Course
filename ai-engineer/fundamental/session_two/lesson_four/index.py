# contoh kode 
retrieved_chunks = [
    {"doc_id": "veritas-104", "text": "RAG combines retrieval and generation.", "score": 0.72},
    {"doc_id": "veritas-101", "text": "RAG combines retrieval and generation.123123", "score": 0.72},
    {"doc_id": "veritas-042", "text": "Chunking strategy affects recall.",      "score": 0.91},
    {"doc_id": "veritas-077", "text": "Embeddings capture semantic meaning.",   "score": 0.85},
]

# --- sorted(): bikin list BARU, data asli tetap utuh ---
# by_score_desc = sorted(retrieved_chunks, key=lambda c: c["score"], reverse=True)
# print(by_score_desc)
# print(by_score_desc[0]["doc_id"])   # veritas-042 (skor tertinggi)
# print(retrieved_chunks[0]["doc_id"])    # veritas-101 <- urutan asli TIDAK berubah

# --- .sort(): mutasi IN-PLACE ---
# retrieved_chunks.sort(key=lambda c: c["score"], reverse=True)
# print(retrieved_chunks[0]["doc_id"])     # veritas-042 <- list asli sekarang ikut berubah

# --- Jebakan klasik: .sort() return None ---
# oops = retrieved_chunks.sort(key=lambda c: c["score"])
# print(oops) # output jadi None, .sort hanya bisa mutasi data langsung di tempat, tidak bisa tampung di variabel lagi

# --- Gabung dengan comprehension (Lesson 3): ambil top-2 doc_id saja ---
# top_2_ids = [c["doc_id"] for c in sorted(retrieved_chunks, key=lambda c: c["score"], reverse=True)[:2]] # mengambil 2 index pertama sebelum index 2
# print(top_2_ids)

# --- Multi-key sort: skor desc, kalau seri baru doc_id asc ---
# multi_sorted = sorted(retrieved_chunks, key=lambda a: (-a["score"], a["doc_id"]))
# print(multi_sorted)
# Trik terakhir: untuk descending pada key numerik, bisa kasih minus (-c["score"]) daripada reverse=True — berguna kalau satu key mau descending tapi key lain tetap ascending dalam satu tuple.

# Challenge

# Pertanyaan 1: Bagaimana kodenya untuk menghasilkan list baru berisi retrieved_chunks yang terurut ascending berdasarkan score (skor terendah di depan), menggunakan sorted() dan key=? Setelah kode itu dijalankan, apakah isi variabel retrieved_chunks yang asli ikut berubah urutannya atau tidak? Jelaskan alasannya?
by_score_desc = sorted(retrieved_chunks, key=lambda c: c["score"])
# print(by_score_desc)
# print(retrieved_chunks)
# tidak berubah, karena sorted ini return ke list baru

# Pertanyaan 2: Bagaimana kodenya untuk mengurutkan retrieved_chunks itu sendiri (in-place) secara descending berdasarkan score, menggunakan .sort() dan reverse=True? Jika setelah itu kamu menulis x = retrieved_chunks.sort(key=..., reverse=True) lalu mencetak print(x), apa yang akan tercetak, dan kenapa?
# retrieved_chunks.sort(key=lambda c: c["score"], reverse=True)
# ini akan mutate data dari retrieved itu sendiri, dan ketika kita coba tampung variabel. Maka hasl nya None, karen .sort return nilai None bukan sebuah list

# Pertanyaan 3: Bagaimana kodenya (bagian key=-nya saja, boleh pakai lambda atau tuple) untuk mengurutkan retrieved_chunks berdasarkan score descending, tapi jika ada dua chunk dengan score yang persis sama, urutan di antara keduanya ditentukan oleh doc_id secara ascending sebagai tie-breaker? 
# asc = rendah ke tinggi | desc = tinggi ke rendah
multi_sort = sorted(retrieved_chunks, key=lambda c: (-c["score"], c["doc_id"]))
# print(multi_sort)
# ini mengurutkan desc by score di tandai dengan tanda minus -, karena quest nya adalah 1 key itu desc dan key lain pakai asc

# Pertanyaan 4: Menggabungkan materi Lesson 3 (comprehension/indexing) dan Lesson 4 (sorting), bagaimana kodenya untuk mendapatkan doc_id dari satu chunk dengan score tertinggi saja dalam satu baris kode? Jelaskan singkat pendekatan yang kamu pakai dan kenapa itu berhasil?
higher_score = [x["doc_id"] for x in sorted(retrieved_chunks, key=lambda x: x["score"], reverse=True)[:1]]
print(higher_score)
# sort key tetap score dengan reverse=True (biar chunk score tertinggi ada di depan),
# tapi value yang diambil di comprehension adalah x["doc_id"] — sort key dan value yang
# diambil itu dua hal beda, gak harus sama. Slice [:1] ambil 1 chunk teratas (score tertinggi).
