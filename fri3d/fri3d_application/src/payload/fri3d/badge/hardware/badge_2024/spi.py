from .pinout import hardware_pinout


class HardwareSPI:
    def __init__(self):
        self.id = 2
        self.baudrate = 80_000_000
        self.pinout = hardware_pinout.pinout_spi


hardware_spi = HardwareSPI()
