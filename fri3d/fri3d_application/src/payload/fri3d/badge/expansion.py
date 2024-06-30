from fri3d.badge.hardware import hardware_capabilities


class Expansion:
    def __init__(self):
        self.uart = None
        self.i2c = None
        # TODO: add I2S

        if hardware_capabilities.i2c:
            from .i2c import i2c
            self.i2c = i2c

        if hardware_capabilities.uart:
            from .uart import uart
            self.uart = uart


expansion = Expansion()
