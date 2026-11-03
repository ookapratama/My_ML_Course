


class Cart:
    def __init__(self, items = None):
        if items is None:
            items = []
        self._items = items

    def add(self, name, price):
        if price <= 0:
            raise ValueError("harga tidak boleh 0 atau dibawah nya")
        self._items.append([name, price])

    @property
    def total(self):
        return sum([x[1] for x in self._items])

    def __len__(self):
        return len(self._items)

def apply_discount(price, percent):
    return int(price - price * (percent / 100))

c = Cart()
c.add("Galon", 6000)
c.add("Gas", 22000)

print(c.total)
print(len(c))
print(apply_discount(10000, 10))
c.add("X", 10)
c.total = 500000
print(c.total)
