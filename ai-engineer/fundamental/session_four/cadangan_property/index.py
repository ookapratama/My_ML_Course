



class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

#    @property
#    def area(self):
#        return self.width * self.height

#r = Rectangle(5,6)
#print(r.area)

#r.width = 10
#print(r.area)

#r.width = 100
#print(r.area)

class Account:
    def __init__(self, balance):
        self.balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("saldo tidak boleh negatif")
        self._balance = value

a = Account(100)
a.balance = 50
print(a.balance)
a.balance = 10


b = Account(-5)

print(b.balance)

