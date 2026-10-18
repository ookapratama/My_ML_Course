class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    def __repr__(self):
        return f"Produk : {self.name} seharga {self.price}"
    
    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price
    
p1 = Product('Galon', '6000')
p2 = Product('Galon', '6000')
p3 = Product('Galon', '18000')

print(p1 == p2)
print(p1 == p3)
print(p1 == 2000)