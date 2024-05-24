from .pinout import hardware_pinout


class HardwareSdCard:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_sd_card
        self.slot = 3
        self.mount_point = '/sd'


hardware_sd_card = HardwareSdCard()
