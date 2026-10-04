import time
from functools import wraps

# Tulis dari blank file, no peeking:

# Buat decorator timing yang print berapa lama function execute. Gunakan time.time() dan @wraps.
def timing(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# Expected output:
@timing
def slow_func():
    time.sleep(1)

@timing
def add(a, b):
    return a + b


slow_func()
# Output: slow_func took 1.00 seconds
add(1, 2)

# Masalah 1: Idenya tepat. Satu detail: start dicatat sebelum func() dan end dicatat sesudahnya. Kalau keduanya di sesudah, selisihnya hampir 0. Durasinya adalah end - start.

# Masalah 2: Benar juga, dan *args dengan **kwargs lebih baik daripada membuat 2 parameter tetap. Kalau kamu menulis wrapper(a, b), decorator-mu hanya bisa dipakai untuk function dengan tepat 2 parameter. Dengan *args, **kwargs, decorator yang sama bisa dipakai untuk function dengan berapa pun parameter.

# Sekarang terapkan keduanya di mini-exercise.py. Lalu uji dengan dua function:
# 1. slow_func() dengan time.sleep(1), yang harus menampilkan sekitar 1.00 seconds.
# 2. add(1, 2), yang harus tetap jalan tanpa error.