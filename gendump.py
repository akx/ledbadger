import os

from ledbadger.message import Message
from ledbadger.protocol import create_usb_payload

messages = [Message() for x in range(8)]
messages[0].enabled = True
messages[1].enabled = True
messages[2].enabled = True
buf = create_usb_payload(messages)
print(buf)

with open('gendump.bin', 'wb') as outf:
    outf.write(bytes(buf))

os.system('xxd gendump.bin | tee g.txt')
