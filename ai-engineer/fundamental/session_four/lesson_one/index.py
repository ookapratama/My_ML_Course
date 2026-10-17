# Lessson 1 : Class

# poin 1
class House:
    address = 'Jl. Jendral Sudirman'
    # print(address)

h1 = House()
# print(h1.address)

# print(House.address)


h2 = House()
h2.address = 'Antang raya'
# print(h2.address)

# poin 2
class Laptop:
    def __init__(self, merk):
        self.merk = merk
        
l1 = Laptop('Lenovo')
# print(l1.merk)

l2 = Laptop('Asus')
# print(l2.merk)

# tantangan 
# a. 
class House:
    def __init__(address):
        self.address = address

h = House("Jl. A")

# b. 
class Order:
    def __init__(self, order_no, status):
        self.order_no = order_no
        self.status = status
        
order1 = Order('001', 'Pending')
order2 = Order('002', 'Paid')

print(f"Orderan : {order1.order_no} berstatus {order1.status}")
print(f"Orderan : {order2.order_no} berstatus {order2.status}")