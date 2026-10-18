
class Order:
    def __init__(self, order_no, status):
        self.order_no = order_no
        self.status = status
    
    def mark_paid(self):
        self.status = 'Paid'
    
    def mark_cancelled(self):
        self.status = 'Cancelled'
        
    def __repr__(self):
        return f"Order no = {self.order_no!r} berstatus {self.status!r}"
        # print(f"Order no = {self.order_no!r} berstatus {self.status!r}")
    
    def __eq__(self, other):
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_no == other.order_no and self.status == other.status
    
    
o = Order('001', 'Pending')
o.mark_paid()
# print(o.status)
# print(o)

o2 = Order('002', 'Pending')
o2.mark_cancelled()
# print(o2.status)
# print(o2)

# A. yg tampil order dengan nomor nya dan status nya dengan menampilkan tipe nilai nya juga dalam hal ini string atau ' '
# B. kalau saya mungkin akan error, karena repr itu harus di return, setelah saya coba, ada error __str__ return non string (type None). yg saya tangkap berarti ketika cetak langsung objek tanpa return di repr maka nilai dari repr itu None karena tidak kita return nilai  nya 


a = Order('001', 'Pending')
b = Order('001', 'Pending')
c = Order('001', 'Paid')
# A.
print(a == b) # ini hasil nya true karena 2 nilai objek yg dikirim sama dengan 2 objek yg kita bandingkan
print(a == c) # false karena status nya beda

# B. hasil nya error karena membandingkan objek dengan int
print(a == 5)
# error nya has no attribut order_no. berarti di nilai other itu tidak memiliki attribut int, karena dari self menerima objek yg mengirim 2 nilai string, sedangkan 5 tidak di kenali dia di assign ke atribut yg mana 

class OrderBatch:
    def __init__(self, orders):
        self.orders = orders
        
    def __len__(self):
        return len(self.orders)

batch = OrderBatch([a, c])
print(len(batch))