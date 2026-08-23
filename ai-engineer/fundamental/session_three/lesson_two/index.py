# Lesson Two - Mutable Default Argument Pitfall
# Example

# Versi Buggy (bnyak baris kode)
def add_chunk_buggy(chunk, history=[]) :
    history.append(chunk)
    return history

chat_1 = add_chunk_buggy("user 1 : siapa presiden RI ?")
chat_2 = add_chunk_buggy("user 2 : ramalam cuaca hari ini ?")

print(chat_2) # -> ['user: siapa presiden RI?', 'user: apa itu machine learning?']  <- BUG
print(chat_1) # -> True (objek yang sama persis)

# Versi Fixed - Pola sentinel None
my = []
def add_chunk_fixed(chunk, history=my) :
    if not history :
        history = []
    history.append(chunk)
    return history
    
chat_1 = add_chunk_fixed("user 1 : siapa presiden RI ?")
chat_2 = add_chunk_fixed("user 2 : ramalam cuaca hari ini ?")

print(chat_2) # -> ['user: apa itu machine learning?']  <- benar, independen
print(chat_1) # -> False
print(my) 

# Challenge
# 1. Kenapa def f(x=[]) bisa menyebabkan bug tapi def f(x=0) atau def f(x="") tidak pernah menyebabkan bug yang sama — apa perbedaan mendasar antara list dengan int/string di sini?
# tipe data nya, list,set,dict itu mutable artinya objek yg dibuat saat pertama define, maka pemanggilan selanjut nya akan memanipulasi data pada objek yang sama
# untuk int/str itu immutable karena nilai nilai yg dikirim dari tiap pemanggilan itu akan mengganti dari nilai sebelum nya
# untuk tuple ini saya masih belum paham, tapi mungkin karena sifat tuple itu sendiri yg tidak bisa di ubah isi nya.

# 2. Kapan tepatnya Python mengevaluasi ekspresi default [] pada def f(items=[]) — setiap kali f() dipanggil, atau momen lain? Sebutkan momennya secara spesifik.
# ketika fungsi itu dipanggil pertama kali dan seterus nya, jadi tiap kita mengirim argumen ke objek itu, pasti akan me mutasi objek yg sama (jadi akan menambah nilai nya, bukan menimpah)
# revisi 1 : pada saat ekspresi itu di define, jadi ketika pertama kali di define, objek langsung ada di memori

# 3. Prediksi output dari kode berikut (tulis outputnya, jelaskan alasannya baris per baris):
def track_embeddings(vector, cache={}): # deklarasi fungsi dengan 2 parameter vectorm dan objek dict bernama cache
    cache[len(cache)] = vector # mapping tiap nilai vector yg masuk ke list panjang cache (index)
    return cache # mengembalikan isi dari cache itu

result_a = track_embeddings("embedding_query_1") # pemanggilan pertama, query 1 dikirim, maka ini akan masuk ke index 0 karena objek masih kosong
result_b = track_embeddings("embedding_query_2") # pemanggilan kedua, query 2 dikirim makan ini akan masuk ke index 1, karena objek sudah memilih nilai, jadi isi nilai nya 1
# print(result_a) # menampilkan key 0 : embedding query 1
# print(result_a == result_b) # menampilkan False, karena isi result a dan b berbeda. a isi nya 1, b isi nya 2
# ini hasil penalaran saya, bukan test compile dulu

# revisi 1 : ternyata saya salah, kanrea sebelum print result a, fungsi di panggil lagi di result b jadi nya hasil result a dan b sama. maka akan menghasilkan True, karena nilai vector yg dikirim di tampung di objek (dict) yang sama

# 4. Kalau kamu ganti if not history: dengan if history is None: pada pola fix, ada satu skenario input dari caller di mana kedua kondisi ini berperilaku BEDA — skenario apa itu, dan kenapa is None lebih benar?

# ketika kirim list kosong, ini di anggap benar, jadi objek di anggap kosong dan menimpa nilai objek itu, maka nya is None lebih benar karena memasutikan objek itu kosong

# revisi 1 : itu karena [] ini masih dianggap sebuah nilai, jadi nya tetap dianggap benar, secara kondisi tetap dianggap benar, tapi itu tidak memastikan bahwa history itu kosong, tapi not history menganggap skenarion caller mengirim [] ini benar. 
# jadi jika case kita buat my_list = [] ini akan benar nilai nya, karena itu adalah sebuah nilai, sedangkan jika pakai none akan salah karena None tidak sama dengan [], 

# revisi 2 : my_list tetap kosong, karena tidak ada nilai yg dimasukkna ke my_list itu

# catatan tambahan (analogi biar gampang inget):
# bayangin caller bawa loker kosong miliknya sendiri (my_list = [], loker #5), terus bilang
# "pakai loker aku buat naruh barang".
# - not history  -> petugas cuma ngecek "loker ini isinya kosong nggak?". karena kosong,
#   dia diam-diam ambil LOKER LAIN buat naruh barang. barang masuk ke loker lain,
#   BUKAN loker #5 yang caller bawa. caller balik ke loker #5, tetap kosong.
# - history is None -> petugas ngecek "kamu beneran nggak bawa loker sama sekali, atau
#   bawa tapi kosong?". karena caller BAWA loker #5 (walau kosong), petugas taruh barang
#   LANGSUNG di loker #5 itu. caller balik, barangnya ada di sana.
# jadi bedanya bukan cuma soal True/False kondisinya, tapi soal object identity: apakah
# fungsi tetap kerja di atas objek yang caller kirim, atau diam-diam ganti ke objek baru.

# 5. Tulis fungsi retrieve_and_append(chunk, history=None) yang menerapkan pola None-sentinel dengan benar — simulasi fungsi RAG yang menambahkan satu retrieved chunk ke list history percakapan lalu mengembalikan list itu — pastikan dua panggilan berturut-turut tanpa argumen history menghasilkan dua list independen.
# def retrieve_and_append(chunk, history=None) :
#     if history is None :
#         history = []
#     history.append(chunk)
#     return history

# chunk_1 = retrieve_and_append("q1 : ibukota indonesia ?")
# chunk_2 = retrieve_and_append("q2 : berapa pulau di indonesian ?")
# chunk_3 = retrieve_and_append("q3 : provinsi sulawesi selatan ?")

# print(chunk_2)
# print(chunk_1)