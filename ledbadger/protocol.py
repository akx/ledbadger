import datetime
import io
from binascii import unhexlify
from typing import List

from construct import Bit, BitStruct, Bitwise, Const, Int16ub, Int8ub, Nibble, Struct

from ledbadger.image import bytes_to_image
from ledbadger.message import Message
from ledbadger.utils import pad_buffer

ShowModeAndSpeed = BitStruct(
    'speed' / Nibble,
    'show_mode' / Nibble,
)

HeaderFormat = Struct(
    'signature' / Const(b'wang'),
    'zero1' / Const(0, Int8ub),
    'brightnesses' / Bitwise(Bit[8]),
    'flashes' / Bitwise(Bit[8]),
    'borders' / Bitwise(Bit[8]),
    'show_modes_and_speeds' / ShowModeAndSpeed[8],
    'lengths' / Int16ub[8],
    'zero2' / Const(0, Int8ub),
    'zero3' / Const(0, Int8ub),
    'address_mode' / Int8ub,
    'address' / Int16ub,
    'zero4' / Const(0, Int8ub),
    'year_div_100' / Int8ub,
    'month' / Int8ub,
    'day' / Int8ub,
    'hour' / Int8ub,
    'minute' / Int8ub,
    'second' / Int8ub,
    'security_code' / Int8ub,
)


def brightness_to_usb(brightness):
    assert 0 <= brightness < 4
    return (brightness << 4) & 240


def create_usb_payload(messages: List[Message], image_height):
    header, image_byteses = get_header_and_bytes(messages, image_height)
    data = pad_buffer(header, 64)

    for index, message in enumerate(messages):
        data += image_byteses[index]

    return data


def get_header_and_bytes(messages, image_height):
    assert len(messages) == 8
    dt = datetime.datetime.now()
    total_length = 0
    image_byteses = [
        (m.get_image_bytes(image_height) if (m.image and m.enabled) else b'')
        for m
        in messages
    ]
    lengths = [0] * 8
    for index, message in enumerate(messages):
        message_len, residue = divmod(len(image_byteses[index]), image_height)
        assert not residue
        num6 = (2560 - total_length if ((total_length + message_len) > 2560) else message_len)
        lengths[index] = num6
        total_length += num6
    assert lengths == [len(buf) / image_height for buf in image_byteses]
    header = HeaderFormat.build(dict(
        brightnesses=[brightness_to_usb(m.brightness) for m in messages],
        flashes=[int(m.flash) for m in messages],
        borders=[int(m.border) for m in messages],
        show_modes_and_speeds=[{
            'show_mode': m.show_mode,
            'speed': m.speed,
        } for m in messages],
        lengths=lengths,
        address_mode=0,
        address=0,
        year_div_100=int(dt.year / 100),
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
        security_code=0,
    ))
    return header, image_byteses


def create_reset_message():
    prelude = unhexlify('020E020E020E02FE')
    return pad_buffer(prelude, 32)


def decode_usb_payload(payload, image_height):
    header = HeaderFormat.parse(payload[:64])
    data = io.BytesIO(payload[64:])
    images = []
    for length in header.lengths:
        n_bytes = length * image_height
        if not n_bytes:
            images.append(None)
        else:
            image_bytes = data.read(n_bytes)
            assert len(image_bytes) == n_bytes, 'short read'
            images.append(bytes_to_image(image_bytes, image_height))
    return (header, images)
