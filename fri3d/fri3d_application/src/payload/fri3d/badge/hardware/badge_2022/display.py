from .pinout import hardware_pinout


class HardwareDisplay:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_display
        self.pixel_clock = 20_000_000
        self.width = 240
        self.height = 240
        self.swap_xy = False
        self.mirror_x = False
        self.mirror_y = False
        self.invert = True
        self.bgr = False


hardware_display = HardwareDisplay()
