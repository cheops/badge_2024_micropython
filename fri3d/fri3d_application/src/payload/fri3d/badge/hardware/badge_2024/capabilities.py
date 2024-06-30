class HardwareCapabilities:
    def __init__(self):
        self.communicator = True
        self.game_on = False
        self.i2c = True
        self.i2s = True
        self.joystick = True
        self.onboard_buttons = True
        self.uart = True


hardware_capabilities = HardwareCapabilities()
