from .pinout import hardware_pinout


class HardwareBuzzer:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_buzzer
        self.freq = 550
        self.duty = 0


hardware_buzzer = HardwareBuzzer()