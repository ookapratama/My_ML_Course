from dataclasses import field
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: int
    
p1 = Product("Galon", 1000)
p2 = Product("Galon", 2000)


print(p1)
print(p1 == p2)

@dataclass
class A:
    name: str
    tags: list = field(default_factory=list)

a1 = A("satu")
a2 = A("dua")
a1.tags.append("X")
a2.tags.append("X")

print(a1.tags)
print(a2.tags)


@dataclass
class B:
    name: str
    qty: int = 1

b1 = B('Galon')


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    
p = Point(1,2)
p = {Point(12000,2)}
# print(p)

s = {Point(1,2), Point(1,2), Point(3,4)}
# print(len(s))

# print(hash("Galon") == hash("Galon"))
# print(hash((1, 2)) == hash((1, 2)))
# print(hash([1, 2]))

from dataclasses import dataclass, asdict, replace

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
d = asdict(p)
q = replace(p, x=9)

print(p)
print(d)
print(q)
print(type(d))