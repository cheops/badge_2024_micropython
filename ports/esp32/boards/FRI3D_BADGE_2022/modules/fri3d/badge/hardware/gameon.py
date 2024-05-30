from .pinout import hardware_pinout


class HardwareGameon:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_gameon


hardware_gameon = HardwareGameon()