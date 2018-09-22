from core import WireType, FieldType
from core import Container

class Required(FieldType):
	def __repr__(self):
		return '<Required{0} {0}>'.format(self.value_type.__name__, self.name)

	def unpack_stream(self, bytes, offset):
		offset2 = self.is_unpackable(bytes, offset)
		return self.value_type.unpack_stream(bytes, offset2)

class Optional(FieldType):
	def __repr__(self):
		return '<Optional{0} {1}>'.format(self.value_type.__name__, self.name)

	def new_default_value(self):
		return None

	def pack_value(self, value):
		if value:
			return super(Optional, self).pack_value(value)
		else:
			return ''

	def unpack_stream(self, bytes, offset):
		offset2 = self.is_unpackable(bytes, offset)
		if offset2:
			return self.value_type.unpack_stream(bytes, offset2)
		else:
			return None, offset

class Repeated(FieldType):
	def __repr__(self):
		return '<Repeated{0} {1}>'.format(self.value_type.__name__, self.name)

	def get_wire_type(self):
		return WireType.LENGHT_DELIMITED

	def new_default_value(self):
		return Container(self.value_type)

	def dumps_value(self, value):
		return value.dumps()

	def dumpo_value(self, value):
		return value.dumpo()

	def pack_payload(self, value):
		return value.pack()

	def unpack_stream(self, bytes, offset):
		offset2 = self.is_unpackable(bytes, offset)
		container = self.new_default_value()
		return container.unpack(bytes, offset2)

