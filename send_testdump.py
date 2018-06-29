from ledbadger.usb import send_payload
from ledbadger.utils import read_hexdump

payload = read_hexdump('data/testdump.txt')
send_payload([payload])
