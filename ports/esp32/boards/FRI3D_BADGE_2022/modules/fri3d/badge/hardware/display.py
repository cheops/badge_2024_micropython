from .pinout import hardware_pinout


class HardwareDisplay:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_display
        self.width = 240
        self.height = 240
        self.rotation = 0
        self.inversion = True
        self.rotations = [(0x00, 240, 240, 0, 0)]


hardware_display = HardwareDisplay()
