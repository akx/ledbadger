import time

import hid

from ledbadger.utils import chunks


def send_payload(payload, yes=False):
    h = hid.device()
    try:
        h.open(0x0416, 0x5020)
        print("Manufacturer: %s" % h.get_manufacturer_string())
        print("Product: %s" % h.get_product_string())
        print("Serial No: %s" % h.get_serial_number_string())

        assert len(payload) % 64 == 0, 'payload must be divisible by 64'

        for chunk in chunks(payload, 64):
            chunk += [0] * (64 - len(chunk))
            assert len(chunk) == 64
            print(chunk)
            if yes:
                h.write(chunk)
            time.sleep(0.1)
    finally:
        h.close()
