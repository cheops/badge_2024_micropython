from .pinout import hardware_pinout


class HardwareGameOn:
    class HardwareGameOnButtons:
        def __init__(self):
            self.pinout = hardware_pinout.pinout_gameon.pinout_buttons
            self.buttons = [
                'a',
                'b',
                'start',
                'select',
                'p0',
                'p1',
                'up',
                'left',
                'down',
                'right',
                'p3',
            ]

    def __init__(self):
        self.buttons = self.HardwareGameOnButtons()


hardware_gameon = HardwareGameOn()
