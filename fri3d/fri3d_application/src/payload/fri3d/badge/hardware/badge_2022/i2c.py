from micropython import const
from .pinout import hardware_pinout


class HardwareI2C:
    def __init__(self):
        self.id = const(0)
        self.pinout = hardware_pinout.pinout_i2c
        self.freq = const(400000)


hardware_i2c = HardwareI2C()
