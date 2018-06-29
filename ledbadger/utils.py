import binascii
import re

from construct import Bit, Bitwise


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
    pad = [value] * (length - len(buffer))
    if pad:
        if isinstance(buffer, bytes):
            pad = bytes(pad)
        buffer = buffer + pad
        assert len(buffer) == length, len(buffer)
    return buffer


def to_bits(bytes):
    return list(Bitwise(Bit[8 * len(bytes)]).parse(bytes))
