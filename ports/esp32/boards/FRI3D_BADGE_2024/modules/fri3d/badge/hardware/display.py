from .pinout import hardware_pinout


class HardwareDisplay:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_display
        self.width = 296
        self.height = 240
        self.rotation = 0
        self.inversion = False
        
        # A rotation table is a list of tuples for each rotation containing the (width, height, x_gap, y_gap, swap_xy, mirror_x, and mirror_y) values for each rotation.
        self.rotations = [(296, 240, 0, 0, True, False, False)]


hardware_display = HardwareDisplay()
