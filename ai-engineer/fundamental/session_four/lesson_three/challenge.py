from dataclasses import asdict
from dataclasses import field
from dataclasses import dataclass



@dataclass
class Chunk:
    text: str
    source: str
    score: float = 0.0
    tags: list = field(default_factory=list)
    
c1 = Chunk("text_chunking", "wikipedia")
c2 = Chunk("text_chunking", "wikipedia")

print(c1 == c2)

c1.tags.append("A")    
print(c1 == c2)

a = asdict(c1)

@dataclass(frozen=True)
class ChunkId:
    source: str
    index: int
    
my_set = {ChunkId("embed-01", 1), ChunkId("embed-01", 1)}
print(my_set)
print(len(my_set))
    