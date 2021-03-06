from proto import *

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
	id      = Required(Unsigned, 2)
	email   = Optional(String, 3)
	addr    = Required(Address, 4)
	phones  = Repeated(PhoneNumber, 5)
	offset  = Optional(Integer, 6)

PhoneNumber.prepare()
Address.prepare()
Person.prepare()

p1 = Person()
p1.name = "a"
p1.id = 150
p1.offset = -7

p1.addr = Address()
p1.addr.main = "home"

phone = p1.phones.add()
phone.number = "999"
phone.type = PhoneType.WORK

phone = p1.phones.add()
phone.number = "998"
phone.type = PhoneType.HOME

import json
dumpj_data = json.dumps(p1.dumpo())
print len(dumpj_data), dumpj_data

dumps_data = p1.dumps() 
print len(dumps_data), dumps_data

packed_data = p1.pack()
print len(packed_data), ','.join('%.2x' % ord(b) for b in packed_data)

p2 = Person()
p2.unpack(packed_data, 0)
print p2.dumps()
