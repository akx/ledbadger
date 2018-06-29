from PIL import Image, ImageOps

from ledbadger.enums import ShowMode
from ledbadger.message import Message
from ledbadger.protocol import create_reset_message, create_usb_payload
from ledbadger.usb import send_payload

messages = [Message() for x in range(8)]

longcat = Image.open('./data/longcat.png').convert('RGB')
longcat = ImageOps.invert(longcat)
longcat = longcat.rotate(90, expand=True)


messages[0].enabled = True
messages[0].speed = 3
messages[0].show_mode = ShowMode.Left
messages[0].image = longcat

buf = create_usb_payload(messages, 11)

# with open('gendump.bin', 'wb') as outf:
#     outf.write(bytes(buf))
#
# header, images = decode_usb_payload(bytes(buf), 11)
# images[0].save('foo.png')
# print(header)
#
# os.system('xxd gendump.bin | tee g.txt')

send_payload([buf, create_reset_message()])
