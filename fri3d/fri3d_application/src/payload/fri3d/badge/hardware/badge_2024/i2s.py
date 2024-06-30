from micropython import const

from .pinout import hardware_pinout


class HardwareI2S:
    def __init__(self):
        self.id = const(1)
        self.pinout = hardware_pinout.pinout_i2s
        self.bits = const(16)
        self.rate = 22_050
        self.ibuf = const(2000)


hardware_i2s = HardwareI2S()
