import base128variant
import zigzag

from core import WireType, ValueType

class String(ValueType):
	@classmethod
	def get_wire_type(cls):
		return WireType.LENGHT_DELIMITED

	@classmethod
	def new_default_value(cls):
		return ""

	@classmethod
	def dumps_value(cls, value):
		return '"{0}"'.format(value)

	@classmethod
	def pack_value(cls, value):
		return base128variant.pack(len(value)) + value	

	@classmethod
	def unpack_stream(cls, bytes, offset):
		value_len, offset = base128variant.unpack(bytes, offset)

		value = bytes[offset:offset + value_len]
		offset += value_len

		return value, offset

class Integer(ValueType):
	@classmethod
	def get_wire_type(cls):
		return WireType.VARIANT

	@classmethod
	def new_default_value(cls):
		return 0

	@classmethod
	def pack_value(cls, value):
		return base128variant.pack(zigzag.encode(value))

	@classmethod
	def unpack_stream(cls, bytes, offset):
		ret, offset = base128variant.unpack(bytes, offset)
		return zigzag.decode(ret), offset

class Unsigned(ValueType):
	@classmethod
	def get_wire_type(cls):
		return WireType.VARIANT

	@classmethod
	def new_default_value(cls):
		return 0

	@classmethod
	def pack_value(cls, value):
		assert(value >= 0)
		return base128variant.pack(value)

	@classmethod
	def unpack_stream(cls, bytes, offset):
		ret, offset = base128variant.unpack(bytes, offset)
		return ret, offset

class Enum(Integer):
	DEFAULT_VALUE = 0
