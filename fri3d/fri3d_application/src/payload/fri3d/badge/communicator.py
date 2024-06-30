from micropython import const

from fri3d.badge.hardware import hardware_capabilities

from .expansion import Expansion


class Communicator(Expansion):
    HID_REPORT_SIZE = const(8)

    HID_KEY_ENTER = const(0x28)
    HID_KEY_ESC = const(0x29)
    HID_KEY_BACKSPACE = const(0x2a)
    HID_KEY_DELETE = const(0x4c)
    HID_KEY_RIGHT = const(0x4f)
    HID_KEY_LEFT = const(0x50)
    HID_KEY_DOWN = const(0x51)
    HID_KEY_UP = const(0x52)
    HID_KEY_HOME = const(0x4a)
    HID_KEY_END = const(0x4d)
    HID_KEY_PAGEUP = const(0x4b)
    HID_KEY_PAGEDOWN = const(0x4e)
    HID_KEY_TAB = const(0x2b)

    def __init__(self):
        super().__init__()

        if not hardware_capabilities.communicator:
            return

        from fri3d.badge.hardware import hardware_communicator

        self._i2c_address = None
        if self.i2c and hardware_communicator.i2c_address in self.i2c.scan():
            # communicator detected
            self._i2c_address = hardware_communicator.i2c_address

        elif self.uart:
            self.uart.init(
                baudrate=hardware_communicator.baudrate,
                bits=hardware_communicator.bits,
                parity=hardware_communicator.parity,
                stop=hardware_communicator.stop
            )

    def get_first_key(self):
        report = None
        if self._i2c_address:
            report = self.i2c.readfrom(self._i2c_address, self.HID_REPORT_SIZE)
        elif self.uart:
            report = self.uart.read(self.HID_REPORT_SIZE)
        if report and len(report) == self.HID_REPORT_SIZE:
            return report[2]

        return None


communicator = Communicator()
