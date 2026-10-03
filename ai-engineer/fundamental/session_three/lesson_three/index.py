# Lesson Three - Closure, Scope, & Lambda
# Example

def make_counter(start: int = 0) :
    count = start 
    # print(f"Root Func Set counter ke {count}")

    def increment() :
        nonlocal count # harus ada ini untuk baca var outer function, perlu define eksplisit
        count += 1
        # print(f"Counter sekarang {count}")
        return count
    
    # print("Root Func return function increment ke kamu(user)")
    return increment

# Eksekusi:
# print("=== Panggil make_counter(10) ===")
c = make_counter(10)
# Output:
# Root set counter ke 10
# Root return function increment ke kamu

# print("\n=== Panggil c() pertama kali ===")
c()
# Output:
# Counter sekarang: 11

# print("\n=== Panggil c() kedua kali ===")
c()
# Output:
# Counter sekarang: 12

# print("\n=== Panggil c() ketiga kali ===")
c()
# Output:
# Counter sekarang: 13 

# Apa yang penting di sini?

# - make_counter(10) selesai, tapi count tetap hidup di memory
# - Setiap kali c() dipanggil, dia ingat nilai count sebelumnya (11, 12, 13...)
# - Itu yang namanya closure: function yang "membawa" variabel dari outer 

# Lambda 
# Di Python:
double = lambda x: x * 2

# Struktur:
# lambda [input] : [output]
#        ↓        ↓
#      parameter  hasil

# Contoh simple:
add = lambda a, b: a + b
# print(add(3, 5))  # Output: 8

# Lambda paling sering dipakai di 3 situasi:

# 1. Sebagai argument di sorted() / map() / filter():
users = [("alice", 30), ("bob", 25), ("charlie", 35)]

# Sorted by umur (gunakan lambda sebagai key)
sorted_by_age = sorted(users, key=lambda u: u[1])
# print(sorted_by_age)
# Output: [('bob', 25), ('alice', 30), ('charlie', 35)]

# 2. Sebagai callback sederhana:
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
# print(doubled)
# Output: [2, 4, 6, 8, 10]

# 3. Assigned ke variabel (jarang, lebih baik pakai def):
square = lambda x: x ** 2
# print(square(5))  # 25


# Challenge - Closure and Lambda
# Bagian 1 — Spot the bug (Closure + Late binding):

def make_multipliers():
    multipliers = []
    for i in range(1, 4):
        multipliers.append(lambda x, i=i: x * i)
    return multipliers

m1, m2, m3 = make_multipliers()
# print(m1(10))  # Print apa? Kenapa?
# print(m2(10))
# print(m3(10))

# Tugas:
# 1. Jalanin kode ini, liat hasilnya
# 2. Jelaskan kenapa output-nya tidak sesuai ekspektasi (harusnya 10, 20, 30)
# 3. Perbaiki dengan menggunakan default argument
# Jawab 
# 1. hasilnya 30 semua
# 2. karena tidak ada nilai parameter yg disimpan dari m* yg dikirim, jadi hasil nya akan sama.  tapi saya tidak paham kenapa lambda bisa membaca nilai dari parameter fungsi m*    
# 3. tambah i=i (params kedua) pada function lambda nya

# Bagian 2 — Tulis Closure (dengan nonlocal):

# Buat function bernama make_tracker() yang return dua function:
# - add(item) — tambah item ke list internal
# - get_all() — return list semua item

# Contoh penggunaan:
# tracker = make_tracker()
# tracker["add"]("apple")
# tracker["add"]("banana")
# print(tracker["get_all"]())  # ['apple', 'banana']

def make_tracker():
    new_item = []
    def add(item) :
        # new_item.append(item) # tanpa nonlocal
        nonlocal new_item
        new_item = new_item + [item] # perlu nonlocal
    def get_all():
        return new_item
    return {"add": add, "get_all": get_all}

tracker = make_tracker()
tracker['add']("apple")
tracker['add']("banana")
# print(tracker["get_all"]())

# mini challenge
# Tulis function make_accumulator(initial: int) yang:
# - Menerima angka awal
# - Return function add(n) yang menambah angka itu ke accumulator
# - Setiap kali add() dipanggil, accumulator bertambah dan return nilai baru

# Contoh:
# acc = make_accumulator(10)
# print(acc(5))   # 15 (10 + 5)
# print(acc(3))   # 18 (15 + 3)
# print(acc(2))   # 20 (18 + 2)

def make_accumulator(initial: int) :
    x = initial # 10
    def add(n) : 
        nonlocal x
        x = x + n
        return x
    return add

acc = make_accumulator(10)
print(acc(5))
print(acc(3))
print(acc(2))