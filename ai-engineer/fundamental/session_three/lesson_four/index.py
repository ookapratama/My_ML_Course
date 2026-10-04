# Lesson Four - Decorators
# Example : 
from functools import wraps
# Buku original
# Wrapping service (decorator)
def wrapping_service(func):
    @wraps(func)
    def wrapper():
        print("Wrapping...")
        result = func()  # Execute buku original
        print("Greeting card added!")
        return result
    return wrapper

@wrapping_service
def book():
    """ This is a book Function """
    return "Buku"


# wrapped_book = wrapping_service(book)
# print(book())
# print(book.__name__)
# print(book.__doc__)
# Output : 
# Wrapping...
# Greeting card added!
# Buku

# Poin 5: Praktik — functools.lru_cache
# Sekarang kita lihat decorator praktis yang udah built-in: lru_cache (Least Recently Used cache).
# Ini decorator yang cache hasil function agar nggak perlu hitung ulang.
# Use case: Fungsi yang expensive (slow) dan bisa di-cache.

from functools import lru_cache

# Tanpa cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Dengan cache
@lru_cache(maxsize=128)  # Cache max 128 hasil terakhir, maksimal cache atau simpan di memori hasil yg fungsi tersebut sudah kerjakan
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

# Test
import time

start = time.time()
# print(fibonacci(35))  # Slow — hitung berkali-kali
# print(f"Tanpa cache: {time.time() - start:.2f}s")

start = time.time()
# print(fibonacci_cached(35))  # Fast — pakai cache
# print(f"Dengan cache: {time.time() - start:.2f}s")

# Challenge: Tulis Decorator Custom untuk Logging
# Buat decorator bernama log_calls yang:
# 1. Print nama function yang dipanggil
# 2. Print argument yang dikirim
# 3. Print hasil return dari function
# 4. Preserve metadata function dengan @wraps

# Contoh penggunaan:
# @log_calls
# def add(a, b):
#     """Add two numbers"""
#     return a + b

# add(3, 5)
# Output:
# Calling add with args=(3, 5), kwargs={}
# add returned: 8

# print(add.__name__)   # Output: add
# print(add.__doc__)    # Output: Add two numbers

from functools import wraps
def Log_calls(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@Log_calls
def add(a,b) :
    """Add two number"""
    return a + b

add(3,5)
print(add.__name__)   # Output: add
print(add.__doc__)  