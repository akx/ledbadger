from ledbadger.protocol import decode_usb_payload
from ledbadger.utils import read_hexdump

payload = read_hexdump('data/testdump.txt')
header, images = decode_usb_payload(payload, 11)

print(header)

for i, image in enumerate(images):
    if image:
        image.save('img%04d.png' % i)
