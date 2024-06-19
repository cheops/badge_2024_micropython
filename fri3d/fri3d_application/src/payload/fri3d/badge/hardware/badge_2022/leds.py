from .pinout import hardware_pinout


class HardwareLEDS:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_leds
        self.amount = 5


hardware_leds = HardwareLEDS()
