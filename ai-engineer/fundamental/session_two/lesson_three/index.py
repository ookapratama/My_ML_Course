# Lesson Three : Comprehensions
# Example :
chunks = [
    {"doc_id": "faq-01", "text": "Cara reset password...", "score": 0.91},
    {"doc_id": "faq-02", "text": "Jam operasional...",     "score": 0.45},
    {"doc_id": "kb-07",  "text": "Kebijakan refund...",    "score": 0.78},
    {"doc_id": "faq-01", "text": "Cara reset password...", "score": 0.88},
]

# a. List comprehension sederhana (transform saja):
scores = [c["score"] for c in chunks]
# print(scores)

# b. List comprehension dengan filter — ambil teks chunk relevan buat prompt LLM:
context_texts = [c["text"] for c in chunks if c["score"] > 0.7]
# print(context_texts)

# c. Dict & set comprehension — beda cuma kurung {} (dan dict butuh key: value):
score_by_doc = {c["doc_id"]: c["score"] for c in chunks}   # dict: doc_id -> score
unique_docs  = {c["doc_id"] for c in chunks}                 # set: dedup otomatis
# print(score_by_doc)
# print(unique_docs)

# ┌───────────┬────────┬────────────┬─────────────────────────────┐
# │  Bentuk   │ Kurung │    Isi     │            Hasil            │
# ├───────────┼────────┼────────────┼─────────────────────────────┤
# │ List comp │ [...]  │ expression │ list (urut, boleh duplikat) │
# ├───────────┼────────┼────────────┼─────────────────────────────┤
# │ Set comp  │ {...}  │ expression │ set (unik)                  │
# ├───────────┼────────┼────────────┼─────────────────────────────┤
# │ Dict comp │ {...}  │ key: value │ dict                        │
# └───────────┴────────┴────────────┴─────────────────────────────┘

# Challenge
retrieved_chunks = [
    {"doc_id": "faq-01", "source": "manual.pdf", "score": 0.92},
    {"doc_id": "faq-02", "source": "manual.pdf", "score": 0.38},
    {"doc_id": "kb-05",  "source": "policy.pdf",  "score": 0.81},
    {"doc_id": "kb-05",  "source": "policy.pdf",  "score": 0.81},
    {"doc_id": "faq-09", "source": "manual.pdf",  "score": 0.65},
]

# Quest 1 :  Bagaimana kodenya (pakai list comprehension) untuk mengambil semua doc_id dari retrieved_chunks menjadi satu list biasa, tanpa filter apa pun?
list_chunks = [x['doc_id'] for x in retrieved_chunks]
print(list_chunks)
# ini mengambil semua nilai dari retrieved_chunks kemudian memaksukan ke variabel x dan mengambil props doc_id saja, jdi yg tampil value dari key doc_id sja

# Quest 2 :  Kamu mau bikin context yang bakal dikirim ke LLM, tapi cuma mau chunk yang cukup relevan. Bagaimana kodenya (list comprehension + filter) untuk mengambil doc_id yang score-nya lebih dari 0.6 saja?
# revisi 1 (salah): relevant_chunks = {x['doc_id']: x['score'] for x in retrieved_chunks if x['score'] > 0.6}
# ^ ini dict comprehension ({key: value}), padahal soal minta list comprehension. juga masukin score
#   sebagai value padahal yg diminta cuma doc_id-nya. filter kondisinya sendiri sudah benar,
#   yang salah cuma bentuk wadahnya (dict vs list).
relevant_chunks = [x['doc_id']  for x in retrieved_chunks if x['score'] > 0.6]
print(relevant_chunks)
# sama seperti quest 1, ini hanya menambahkan kondisi untuk filter doc_id dengan kriteria score tertentu
# revisi 2 (benar): sudah list comprehension (bukan dict), ambil doc_id saja sesuai yg diminta,
# filter score > 0.6 tepat.

# Quest 3 :  Bagaimana kodenya (set comprehension) untuk mengambil semua nilai source yang unik dari retrieved_chunks? Setelah itu, berapa jumlah item di hasilnya, dan kenapa jumlahnya lebih sedikit dibanding jumlah dictionary di retrieved_chunks?
# revisi 1 (salah): unique_chunks = {x['doc_id'] for x in retrieved_chunks}
# ^ field salah — ambil doc_id, padahal soal minta source.
# revisi 2 (salah): unique_chunks = {x['score'] for x in retrieved_chunks}
# ^ ganti field lagi tapi masih salah — ambil score, bukan source. len()-nya kebetulan
#   angkanya "masuk akal" (4, karena ada 2 chunk dgn score 0.81 yg sama), tapi itu jawaban
#   utk pertanyaan yg salah, bukan pertanyaan yg diminta soal.
unique_chunks = {x['source'] for x in retrieved_chunks}
print(len(unique_chunks))
# di bungkus dengan {} set, ini menghilangkan duplikat karena kita pakai set — set nggak bisa
# menyimpan dua nilai yang sama persis, bukan karena "diacak"/random. urutan yang nggak
# dijamin (unordered) itu hal yang beda dari alasan kenapa duplikat hilang.
# revisi 3 (benar) : field-nya sekarang source sesuai soal. hasilnya 2 (bukan 5), karena dari
# 5 chunk, source "manual.pdf" muncul 3x dan "policy.pdf" muncul 2x — masing-masing kolaps
# jadi 1 nilai unik lewat set, jadi totalnya 2 item.

# Quest 4 :  Perhatikan potongan kode berikut:
doc_ids = ["faq-01", "faq-02", "kb-05"]
[d.upper() for d in doc_ids]
# Setelah baris kedua dijalankan, isi doc_ids jadi apa? Kenapa begitu?
# answer : tidak terjadi apa apa pada doc_ids karena hasil pada baris kedua di buang setelah di ubah, karena nila nya tidak di simpan di variabel manapun atau tidak tempat untuk menampung hasil dari comprehensions nya. jadi nya tidak ada yg berubah pada doc_ids. kecuali saya tmbahkan perintah print, maka hasil nya pasti tampil (ini belum saya jalankan, tapi berdasarkan penalaran saya)
