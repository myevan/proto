def encode(value):
    return (value << 1 if value > 0 else (-value << 1) - 1) if value else 0

def decode(encoded_value):
    return -((encoded_value + 1) >> 1) if encoded_value & 1 else encoded_value >> 1

if __name__ == '__main__':
    assert(encode(-1) == 1)
    assert(encode(0) == 0)
    assert(encode(+1) == 2)

    assert(decode(0) == 0)
    assert(decode(1) == -1)
    assert(decode(2) == +1)

    for i in range(-10, 10):
        assert(decode(encode(i)) == i)
