import hid
import time
from binascii import hexlify

from ledbadger.utils import chunks, pad_buffer


def send_payload(buffers):
    h = hid.device()
    try:
        h.open(0x0416, 0x5020)
        for bi, buffer in enumerate(buffers):
            for ci, chunk in enumerate(chunks(buffer, 64)):
                # The buffer must be sent in messages of 64 bytes,
                # each prefixed by a single null byte.
                chunk = pad_buffer(chunk, 64)
                assert h.write([0] + chunk) == 65
                print(bi, ci, hexlify(bytes(chunk)))
                time.sleep(0.3)
    finally:
        h.close()
