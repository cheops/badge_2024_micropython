from machine import Pin
from neopixel import NeoPixel

from fri3d.badge.hardware import hardware_leds


class Leds(NeoPixel):
    def __init__(self):
        super().__init__(
            Pin(hardware_leds.pinout.pin, Pin.OUT),
            hardware_leds.amount,
        )

        # Clear the pixels on import
        for id in range(hardware_leds.amount):
            self[id] = (0, 0, 0)

        self.write()


leds = Leds()
