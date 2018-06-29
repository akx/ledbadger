from PIL import Image
from construct import bits2integer

from ledbadger.utils import chunks, to_bits


def image_to_bytes(image):
    # The bits are arranged in the payload
    # as (8 x H) chunks following each other.
    # This means the image's width must MOD 8 = 0.
    width, height = image.size
    arr = []
    data = image.convert('1').load()
    for x_offset in range(0, width, 8):
        for y in range(height):
            bits = [(1 if data[(x_offset + x, y)] else 0) for x in range(8)]
            arr.append(bits2integer(bits))
    return bytes(arr)


def bytes_to_image(bytes, height):
    width = int(len(bytes) / height)
    image = Image.new('1', (width * 8, height))
    data = image.load()
    chunk_iter = chunks(to_bits(bytes), 8)
    x_offset = 0
    while True:
        for y in range(height):
            for x, b in enumerate(next(chunk_iter)):
                data[(x_offset + x, y)] = (255 if b else 0)
        x_offset += 8
        if x_offset >= image.width:
            break
    return image
