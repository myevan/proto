# proto

## scheme

```python
class PhoneType(Enum):
	MOBILE = 0
	HOME = 1
	WORK = 2

class PhoneNumber(Message):
	number 	= Required(String, 1)
	type 	= Optional(PhoneType, 2)

class Address(Message):
	main 	= Required(String, 1)
	sub 	= Optional(String, 2)

class Person(Message):
	name    = Required(String, 1)
	id      = Required(Integer, 2)
	email   = Optional(String, 3)
	addr    = Required(Address, 4)
	phones  = Repeated(PhoneNumber, 5)
	offset  = Optional(Integer, 6)
```

## packing

```python
p1 = Person()
p1.name = "a"
p1.offset = -7

p1.addr = Address()
p1.addr.main = "home"

phone = p1.phones.add()
phone.number = "999"
phone.type = PhoneType.WORK

phone = p1.phones.add()
phone.number = "998"
phone.type = PhoneType.HOME

packed_data = p1.pack()
```

## result

### json dumped

235 bytes

```python
{"__name__": "Person", "name": "a", "id": 150, "addr": {"__name__": "Address", "main": "home"}, "phones": [{"__name__": "PhoneNumber", "number": "999", "type": 2}, {"__name__": "PhoneNumber", "number": "998", "type": 1}], "offset": -7}
```

### string dumped

45 bytes

```
("a",150,,("home",),[("999",2),("998",1)],-7)
```

### proto packed

31 bytes

```
0a,01,61,10,96,01,22,0a,04,68,6f,6d,65,2a,02,0a,03,39,39,39,10,04,0a,03,39,39,38,10,02,30,0d
```

## unpacking

```python
p2 = Person()
p2.unpack(packed_data, 0)
```