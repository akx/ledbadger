from ledbadger.enums import ShowMode
from ledbadger.image import image_to_bytes


class Message:
    def __init__(
        self,
        brightness=0,
        show_mode=ShowMode.Left,
        speed=8,
        enabled=False,
        flash=False,
        border=False,
    ):
        self.brightness = brightness
        self.show_mode = show_mode
        self.speed = speed
        self.enabled = bool(enabled)
        self.flash = bool(flash)
        self.border = bool(border)
        self.image = None

    def get_image_bytes(self, height):
        assert self.image.size[1] == height
        return image_to_bytes(self.image)
