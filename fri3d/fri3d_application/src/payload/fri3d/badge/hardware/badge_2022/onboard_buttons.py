from .pinout import hardware_pinout


class HardwareOnboardButtons:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_onboard_buttons
        self.buttons = [
            'boot',
        ]


hardware_onboard_buttons = HardwareOnboardButtons()
