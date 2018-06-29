import binascii
import re


def read_hexdump(filename):
    with open(filename, 'r') as infp:
        return binascii.unhexlify(re.sub('\s+', '', infp.read()))


def chunks(iterable, chunk_size):
    chunk = []
    for item in iterable:
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
        chunk.append(item)
    if chunk:
        yield chunk


def pack_to_byte(bits):
    byte = 0
    for bit in bits:
        byte = (byte << 1) | (1 if bit else 0)
    return byte


def pad_buffer(buffer, length, value=0):
    buffer = buffer + [value] * (length - len(buffer))
    assert len(buffer) == length
    return buffer
