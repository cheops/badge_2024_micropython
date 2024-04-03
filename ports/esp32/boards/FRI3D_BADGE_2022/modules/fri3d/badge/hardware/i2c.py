from .pinout import hardware_pinout


class HardwareI2C:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_i2c


hardware_i2c = HardwareI2C()
