# Lesson One - *args, **kwargs, dan Keyword-Only Arguments
# Example 
def call_llm(*, model, temperature=0.7, **extra_params) :
    # model & temperature: WAJIB keyword-only (ada '*' di depan) — mencegah caller salah urutan.
    # **extra_params: menampung semua keyword lain (top_p, max_tokens, stop, dst) jadi satu dict.
    print(f"Calling model={model} with temperatur={temperature}")
    print(f"Extra params: {extra_params}")

call_llm(model="claude-sonnet-4.5", temperature=0.2, top_p=0.9, max_tokens=500)
# -> extra_params otomatis jadi {"top_p": 0.9, "max_tokens": 500}

# ERROR — model & temperature keyword-only, nggak boleh positional:
# call_llm("claude-sonnet-4.5", 0.2)

def merge_chunks(*chunks, seperator="\n\n") :
    # *chunks: nampung sejumlah RAG text chunk (positional, jumlah bebas)
    return seperator.join(chunks)

context = merge_chunks("Chunk A tentang refund policy.", "Chunk B tentang shipping.", "Chunk C tentang warranty.")
print(context)

# Challenge
# 1. Apa perbedaan mendasar antara cara *args menampung argumen dibanding **kwargs, dalam hal tipe data yang dihasilkan?
# *args menampung semua argumen positional atau nilai nya dan disimpan tampung dalam bentuk tuple 
# **kwargs itu menampung semua key-value ke dalam bentuk dict, 

# 2. Kalau kamu punya def f(*, timeout=5): ..., kenapa f(10) menghasilkan error, dan bagaimana cara pemanggilan yang benar?
# error karena parameter pertama * itu hanyalah pemisah, untuk mengirim nilai 10 itu harus menggunakan key=value, karena tanda * sudah di deklarasikan di tepat di parameter pertama
# fix : 
def f(*, timeout=5) :
    print(timeout)
f(timeout=10)

# 3. Tulis fungsi kecil def build_rag_prompt(*sources, **options) yang menerima sejumlah string sumber (positional, jumlah bebas) dan opsi tambahan seperti style="formal" lewat keyword — lalu print hasil gabungannya dalam format bebas.
def build_rag_prompt(*sources, **options) :
    print(f"sources : {sources}")
    print(f"options : {options}")

build_rag_prompt("doc_1", "doc_2", "doc_3", style="formal", color="grey", font="arial")


# 4. Spot the bug — kenapa kode berikut akan error saat dijalankan, dan apa fix-nya?
# def call_llm(model, *, temperature=0.7, **extra):
#     pass

# call_llm("gpt-4", 0.9, top_p=0.95)
# error karena parametr kedua mengirim 0.9, seharusnya menambah keyowrd temperatur untuk mengirim nilai itu, karena tanda * args di pangil sebelum temperature, kemungkinan itu untuk menampung data" model selain model yg diketahui. jadi dipakai *
# karena * sudah di panggil, jadi parameter selanjut nya harus memakai key=value, seterusnya smpai **extra jika ada tmbahan

# koreksi: kalimat "kemungkinan itu untuk menampung data model selain model yg diketahui" itu salah konsep.
# * bare (tanpa nama) di sini TIDAK menampung apa-apa sama sekali — beda dengan *args/*sources/*chunks yang
# punya nama dan memang aktif nampung nilai jadi tuple. * bare cuma penanda "positional berhenti di sini,
# semua parameter setelah ini wajib keyword". Jadi call_llm("gpt-4", 0.9, top_p=0.95) error BUKAN karena
# * "menampung" 0.9 ke suatu tempat, tapi karena setelah `model` (satu-satunya slot positional) tidak ada
# *args bernama yang bisa nampung 0.9 — Python nggak tahu taruh di mana, makanya TypeError.
# kalimat penutup di atas ("karena * sudah dipanggil, parameter selanjutnya harus key=value") sudah benar
# dan itu cukup untuk jawab root cause-nya sendiri.

# fix
def call_llm(model, *, temperature=0.7, **extra):
    pass

call_llm("gpt-4", temperature=0.9, top_p=0.95)
