from micropython import const

from .pinout import hardware_pinout


class HardwareUART:
    def __init__(self):
        self.id = const(0)
        self.pinout = hardware_pinout.pinout_uart


hardware_uart = HardwareUART()
