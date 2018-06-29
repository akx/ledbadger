import datetime
from binascii import unhexlify

from ledbadger.utils import pack_to_byte, pad_buffer


def brightness_to_usb(brightness):
    assert 0 <= brightness < 4
    return (brightness << 4) & 240


def showmode_and_speed_to_usb(showmode, speed):
    assert 0 <= showmode < 16
    assert 0 <= speed < 16
    return showmode | (speed << 4)


def create_usb_payload(messages):
    assert len(messages) == 8
    data = list(b'wang')
    data.append(0)  # always zero
    data.extend([brightness_to_usb(m.brightness) for m in messages])  # brightnesses x 8
    data.append(pack_to_byte([m.flash for m in messages]))  # flash values x 8
    data.append(pack_to_byte([m.border for m in messages]))  # lamp (border) values x 8
    data.extend([showmode_and_speed_to_usb(m.showmode, m.speed) for m in messages])  # showmodes and speeds x 8

    total_length = 0
    length_array = [0] * 8

    for index, message in enumerate(messages):
        message_len = (message.length if message.enabled else 0)
        num6 = (2560 - total_length if ((total_length + message_len) > 2560) else message_len)
        length_array[index] = num6
        total_length += num6
        data.append(num6 >> 8)
        data.append(num6 & 0xFF)

    data.extend([0, 0])  # always zero

    # address bytes --
    # "write address" mode = 0x1 / address high byte / address low byte
    # "send to address" mode = 0x2 / address high byte / address low byte
    # else: 0x0 / 0x0 / 0x0
    data.extend([0, 0, 0])

    data.append(0)  # always zero

    # current datetime
    dt = datetime.datetime.now()
    data.append(int(dt.year / 100))
    data.append(dt.month)
    data.append(dt.day)
    data.append(dt.hour)
    data.append(dt.minute)
    data.append(dt.second)

    # "security code" -- either 0 or the first byte received from a
    # mysterious network connection after the word "leshan"
    data.append(0)

    data = pad_buffer(data, 64)

    image_height = 12

    for index, message in enumerate(messages):
        if length_array[index] == 0:
            continue
        buf = [0] * (length_array[index] * image_height)
        for i, x in enumerate(buf[:]):
            buf[i] = (255 if i % 2 else 0)
        data.extend(buf)

    return data


def create_reset_message():
    prelude = unhexlify('020E020E020E02FE')
    return pad_buffer(prelude, 64)
