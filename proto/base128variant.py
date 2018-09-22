import struct

PACK_FORMATS = [
    '',
    '<B',
    '<BB',
    '<BBB',
    '<BBBB',
    '<BBBBB',
    '<BBBBBB',
    '<BBBBBBB',
    '<BBBBBBBB',
    '<BBBBBBBBB',
    '<BBBBBBBBBB',
]

def gen_encoded_values(value):
    assert(value >= 0)

    remain = value & 0x7f
    value >>= 7

    while value:
        yield 0x80 | remain
        remain = value & 0x7f
        value >>= 7

    yield remain

def pack(value):
    encoded_values = tuple(gen_encoded_values(value))
    return struct.pack(PACK_FORMATS[len(encoded_values)], *encoded_values)

def unpack(bytes, offset):
    decoded_value = 0
    step = 0

    while offset < len(bytes):
        encoded_value = ord(bytes[offset])
        offset += 1

        if encoded_value & 0x80:
            decoded_value |= (encoded_value & 0x7f) << (7 * step)
            step += 1
        else:
            decoded_value |= encoded_value << (7 * step)
            step += 1
            break

    return decoded_value, offset
