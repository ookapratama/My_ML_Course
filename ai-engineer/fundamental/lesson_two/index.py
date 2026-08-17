# Session 2 
# Lesson 1 - Core Data Structures
# chunk_sources = [
#     ("doc1.pdf", 3),
#     ("doc2.pdf", 7),
#     ("doc1.pdf", 3),
#     ("doc3.pdf", 1),
# ]

# seen = set()
# result = []


# for item in chunk_sources :
#     if item not in seen :
#         result.append(item)
#         seen.add(item)
# print(result)

# Lesson 2 - Slicing & Unpacking
# ambil top 3
ranked_results = ["doc_9", "doc_2", "doc_5", "doc_7", "doc_1", "doc_3"]
top_3 = ranked_results[:3]
# print(top_3)

# balik dari urutan skor paling rendah
reversed_results = ranked_results[::-1]
# print(reversed_results)

# Unpacking : pisah kan best match/result dengan data yg lain
best_result, *remaining_candidates = ranked_results
# print(best_result)
# print(remaining_candidates)

# Kombinasi : ambil top-5, unpack best + runner up + sisa nya
top_5 = ranked_results[:5]
best, second, *others = top_5
# print(best, second, others)

# Challenge
# Tantangan Lesson 2: Slicing & Unpacking di Konteks Veritas
# Bayangkan begini: retriever Veritas baru saja mengembalikan daftar hasil pencarian, sudah terurut dari yang paling relevan sampai paling tidak relevan.
results = ["doc_A", "doc_B", "doc_C", "doc_D", "doc_E", "doc_F", "doc_G", "doc_H", "doc_I", "doc_J"]

# Quest 1 : ambil 3 teratas
top_3 = results[:3]
# print(top_3)

# Quest 2 : 
# a. Kamu mau ambil hasil yang paling tidak relevan (elemen terakhir di list) tanpa menghitung manual panjang list-nya — pakai index negatif. Bagaimana kodenya?
unrelevant_match = results[-1]
# print(unrelevant_match) 

# b. 
reversed_results = results[::-1]
# print(reversed_results[0])
# Menurutmu, apa yang bakal dicetak ke layar? Kenapa jawabannya itu?
# ini aka me reverse data list nya dari belakang, otomatis data yg di copy dimuat dari doc_J, dan ketika di panggil index 0 maka yg tampil adalah doc_J

# Quest 3 :
# Temanmu nulis kode buat pisahin top-1, top-2, dan sisanya:
# top_result, second_result, *rest = results
# Lalu di file lain, dia nulis ini buat skenario berbeda:
# first, *middle, *last = results

# a. Baris pertama — menurutmu valid atau error? Kalau valid, apa isi rest setelah baris itu dijalankan?
# a. : Baris pertama valid, dan isi dari rest nya adalah doc_C dan seterusnta smpai doc_J, karena doc A dan B telah di simpan di variabel lain

# b. Baris kedua — apakah ini bakal jalan tanpa error? Kalau tidak, kenapa Python melarangnya?
# b. : error walaupun belum dijalankan, karena unpacking star hanya bisa 1 deklarasi dalam 1 sintaks. itu aturan untuk unpacking di python

# Bonus Check (Boleh di jawab singkat)
# top3 = results[:3]
# top3.append("doc_X")
# print(len(results))
# Apakah len(results) tetap 10, atau berubah jadi 11? Kenapa?
# Tetap 10 karena top_3 itu meng copy data dari results, bukan mengubah dari results itu sendiri, jadi jawaban tetap 1- untuk results, untuk top_3 jadi 4, karena penambahan doc_X yg di append di top_3
