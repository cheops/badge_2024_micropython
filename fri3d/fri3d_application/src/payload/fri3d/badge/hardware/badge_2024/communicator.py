from micropython import const


class HardwareCommunicator:
    def __init__(self):
        self.baudrate = const(115200)
        self.bits = const(8)
        self.parity = None
        self.stop = const(1)
        self.i2c_address = const(0x38)


hardware_communicator = HardwareCommunicator()
