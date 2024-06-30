class HardwareCapabilities:
    def __init__(self):
        self.communicator = False
        self.game_on = True
        self.i2c = True
        self.i2s = False
        self.joystick = False
        self.onboard_buttons = True
        self.uart = False


hardware_capabilities = HardwareCapabilities()
