import inspect
import struct
import base128variant

from collections import OrderedDict

class WireType(object):
	VARIANT = 0
	FIXED_64 = 1
	LENGHT_DELIMITED = 2
	START_GROUP = 3
	END_GROUP = 4
	FIXED_32 = 2

class ValueType(object):
	DEFUALT_VALUE = None

	@classmethod
	def dumps_value(cls, value):
		return str(value)

	@classmethod
	def dumpo_value(cls, value):
		return value

class FieldType(object):
	_global_id = 1

	@staticmethod
	def alloc_id():
		ret_id = FieldType._global_id
		FieldType._global_id += 1
		return ret_id

	def __init__(self, value_type, index):
		self.name = ''
		self.value_type = value_type
		self.index = index
		self.id = self.alloc_id()

	def __repr__(self):
		return '<Field {0}>'.format(self.name)

	def set_name(self, name):
		self.name = name

	def get_wire_type(self):
		return self.value_type.get_wire_type()

	def new_default_value(self):
		return self.value_type.new_default_value()

	def dumps_value(self, value):
		return self.value_type.dumps_value(value)

	def dumpo_value(self, value):
		return self.value_type.dumpo_value(value)

	def pack_value(self, value):
		def gen_pack():
			yield base128variant.pack((self.index << 3) | self.get_wire_type())
			yield self.pack_payload(value)

		return ''.join(gen_pack())

	def pack_payload(self, value):
		return self.value_type.pack_value(value)

	def is_unpackable(self, bytes, offset):
		head, offset2 = base128variant.unpack(bytes, offset)
		if ((head >> 3) == self.index):
			if ((head & 7) == self.get_wire_type()):
				return offset2
		
		return None

class MessageType(object):
	@classmethod
	def prepare(cls):
		def collect_field_types():
			for field_name, field_type in inspect.getmembers(cls):
				if isinstance(field_type, FieldType):
					field_type.set_name(field_name)
					yield field_type

		cls.field_types = list(sorted(collect_field_types(), key=lambda x: x.id))

	@classmethod
	def get_wire_type(cls):
		return WireType.LENGHT_DELIMITED

	@classmethod
	def new_default_value(cls):
		return cls()

	@classmethod
	def dumps_value(cls, value):
		def gen_dumps():
			for field_type in cls.field_types:
				field_value = getattr(value, field_type.name)
				if field_value is None:
					yield '' # None
				else:
					yield field_type.dumps_value(field_value)

		return '(' + ','.join(str(data) for data in gen_dumps()) + ')'

	@classmethod
	def dumpo_value(cls, value):
		ret = OrderedDict()
		ret['__name__'] = cls.__name__

		for field_type in cls.field_types:
			field_value = getattr(value, field_type.name)
			if field_value is None:
				pass
			else:
				ret[field_type.name] = field_type.dumpo_value(field_value)

		return ret		

	@classmethod
	def pack_value(cls, value):
		return value.pack()

	@classmethod
	def unpack_stream(cls, bytes, offset):
		value = cls()
		meta = super(cls, value)
		for field_type in cls.field_types:
			field_value, offset2 = field_type.unpack_stream(bytes, offset)
			if offset2 is None:
				meta.__setattr__(field_type.name, field_type.new_default_value())
			else:
				meta.__setattr__(field_type.name, field_value)
				offset = offset2

		return value, offset 

	def __init__(self):
		for field_type in self.__class__.field_types:
			super(MessageType, self).__setattr__(field_type.name, field_type.new_default_value())

	def __repr__(self):
		return '<{0}>'.format(self.__class__.__name__)

	def __setattr__(self, name, value):
		field_type = getattr(self.__class__, name)
		super(MessageType, self).__setattr__(field_type.name, value)

	def dumps(self):
		return self.dumps_value(self)

	def dumpo(self):
		return self.dumpo_value(self)

	def pack(self):
		return ''.join(field_type.pack_value(getattr(self, field_type.name)) for field_type in self.__class__.field_types)

	def unpack(self, bytes, offset):
		meta = super(self.__class__, self)
		for field_type in self.__class__.field_types:
			field_value, offset2 = field_type.unpack_stream(bytes, offset)
			if offset2 is None:
				meta.__setattr__(field_type.name, field_type.new_default_value())
			else:
				meta.__setattr__(field_type.name, field_value)
				offset = offset2

		return offset 

class Container(object):
	def __init__(self, value_type):
		self.value_type = value_type
		self.values = []

	def __repr__(self):
		return '<Container:{0}>'.format(self.value_type.__name__)

	def __getitem__(self, index):
		return self.values[index]

	def add(self):
		new_value = self.value_type()
		self.values.append(new_value)
		return new_value

	def dumps(self):
		return '[' + ','.join(self.value_type.dumps(value) for value in self.values) + ']'

	def dumpo(self):
		return [self.value_type.dumpo(value) for value in self.values]

	def pack(self):
		def gen_pack():
			yield base128variant.pack(len(self.values))

			for value in self.values:
				yield self.value_type.pack(value) 

		return ''.join(gen_pack())

	def unpack(self, bytes, offset):
		value_len, offset = base128variant.unpack(bytes, offset)

		for index in range(value_len):
			value, offset = self.value_type.unpack_stream(bytes, offset)
			self.values.append(value)

		return self, offset

