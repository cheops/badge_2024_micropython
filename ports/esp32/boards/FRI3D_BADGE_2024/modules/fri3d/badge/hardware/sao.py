from .pinout import hardware_pinout


class HardwareSao:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_sao


hardware_sao = HardwareSao()