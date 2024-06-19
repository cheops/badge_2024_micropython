from .pinout import hardware_pinout


class HardwareSAO:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_sao


hardware_sao = HardwareSAO()
