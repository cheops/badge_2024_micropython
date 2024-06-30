from micropython import const
from fri3d.badge.hardware.pin import HardwarePinInput


class HardwarePinout:
    class PinoutBuzzer:
        def __init__(self):
            self.pin_buzzer = const(46)

    class PinoutDisplay:
        def __init__(self):
            self.pin_rst = const(48)
            self.pin_dc = const(4)
            self.pin_cs = const(5)

    class PinoutI2C:
        def __init__(self):
            self.sda = const(9)
            self.scl = const(18)

    class PinoutI2S:
        def __init__(self):
            self.sck = const(2)
            self.ws = const(47)
            self.sd = const(16)

    class PinoutJoystick:
        def __init__(self):
            self.pin_joystick_x = const(1)
            self.pin_joystick_y = const(3)

    class PinoutLEDS:
        def __init__(self):
            self.pin = const(12)

    class PinoutOnboardButtons:
        def __init__(self):
            self.pin_a = HardwarePinInput(const(39), True)
            self.pin_b = HardwarePinInput(const(40), True)
            self.pin_x = HardwarePinInput(const(38), True)
            self.pin_y = HardwarePinInput(const(41), True)
            self.pin_menu = HardwarePinInput(const(45), True)
            self.pin_start = HardwarePinInput(const(0), False)

    class PinoutSAO:
        def __init__(self, leds):
            self.gpio1 = leds.pin
            self.gpio2 = const(13)

    class PinoutSPI:
        def __init__(self):
            self.pin_mosi = const(6)
            self.pin_miso = const(8)
            self.pin_sck = const(7)

    class PinoutUART:
        def __init__(self):
            self.tx = const(43)
            self.rx = const(44)

    def __init__(self):
        self.pinout_buzzer = self.PinoutBuzzer()
        self.pinout_display = self.PinoutDisplay()
        self.pinout_i2c = self.PinoutI2C()
        self.pinout_i2s = self.PinoutI2S()
        self.pinout_joystick = self.PinoutJoystick()
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_onboard_buttons = self.PinoutOnboardButtons()
        self.pinout_sao = self.PinoutSAO(self.pinout_leds)
        self.pinout_spi = self.PinoutSPI()
        self.pinout_uart = self.PinoutUART()


hardware_pinout = HardwarePinout()
