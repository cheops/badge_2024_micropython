from micropython import const
from fri3d.badge.hardware.pin import HardwarePinInput


class HardwarePinout:
    class PinoutLEDS:
        def __init__(self):
            self.pin = const(12)

    class PinoutSPI:
        def __init__(self):
            self.pin_mosi = const(6)
            self.pin_miso = const(8)
            self.pin_sck = const(7)

    class PinoutDisplay:
        def __init__(self):
            self.pin_rst = const(48)
            self.pin_dc = const(4)
            self.pin_cs = const(5)

    class PinoutSAO:
        def __init__(self, leds):
            self.gpio1 = leds.pin
            self.gpio2 = const(13)

    class PinoutOnboardButtons:
        def __init__(self):
            self.pin_a = HardwarePinInput(const(39), True)
            self.pin_b = HardwarePinInput(const(40), True)
            self.pin_x = HardwarePinInput(const(38), True)
            self.pin_y = HardwarePinInput(const(41), True)
            self.pin_menu = HardwarePinInput(const(45), True)
            self.pin_start = HardwarePinInput(const(0), False)

    class PinoutJoystick:
        def __init__(self):
            self.pin_joystick_x = const(1)
            self.pin_joystick_y = const(3)

    class PinoutBuzzer:
        def __init__(self):
            self.pin_buzzer = const(46)

    def __init__(self):
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_spi = self.PinoutSPI()
        self.pinout_display = self.PinoutDisplay()
        self.pinout_sao = self.PinoutSAO(self.pinout_leds)
        self.pinout_onboard_buttons = self.PinoutOnboardButtons()
        self.pinout_joystick = self.PinoutJoystick()
        self.pinout_buzzer = self.PinoutBuzzer()


hardware_pinout = HardwarePinout()
