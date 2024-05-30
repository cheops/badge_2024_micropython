from .pinout import hardware_pinout


class HardwareJoystick:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_joystick


hardware_joystick = HardwareJoystick()