from pydantic import Field, BaseModel, ValidationError


class Product(BaseModel):
    name: str
    price: int = Field(gt=0)
    stock: int = 0


p = Product(name="Galon", price=100000)
print(p.model_dump())

try:
    #p1 = Product(name="Galon", price=-100)
    #print(p1)

    p2 = Product(name="Galon", price=10)
    print(p2)

except ValidationError as e:
    print(e)

class Item(BaseModel):
    name: str
    price: int = Field(gt=0)

class Order(BaseModel):
    order_no: str
    items: list[Item]

raw = '{"order_no": "A1", "items": [{"name": "Galon", "price": 6000}, {"name": "Galon", "price": 23000}]}'
order = Order.model_validate_json(raw)

print(order)



#try:
#    Product(name="Galon", price="abc")
#except ValidationError as e:
#    print(e)
