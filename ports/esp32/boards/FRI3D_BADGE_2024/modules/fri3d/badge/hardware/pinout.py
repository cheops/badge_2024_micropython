from micropython import const
from machine import Pin


class HardwarePinout:
    class PinoutLEDS:
        def __init__(self):
            self.pin = Pin(12, Pin.OUT)

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
        def __init__(self, leds: PinoutLEDS):
            self.gpio1 = leds.pin
            self.gpio2 = const(13)

    class PinoutButtons:
        def __init__(self):
            self.pin_buttons = {
                'a': Pin(39, Pin.IN, Pin.PULL_UP),
                'b': Pin(40, Pin.IN, Pin.PULL_UP),
                'x': Pin(38, Pin.IN, Pin.PULL_UP),
                'y': Pin(41, Pin.IN, Pin.PULL_UP),
                'menu': Pin(45, Pin.IN, Pin.PULL_UP),
                'start': Pin(0, Pin.IN)  # has external pullup
            }

    class PinoutJoystick:
        def __init__(self):
            self.pin_joystick_x = const(1)
            self.pin_joystick_y = const(3)

    def __init__(self):
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_spi = self.PinoutSPI()
        self.pinout_display = self.PinoutDisplay()
        self.pinout_sao = self.PinoutSAO(self.pinout_leds)
        self.pinout_buttons = self.PinoutButtons()
        self.pinout_joystick = self.PinoutJoystick()


class HardwareCapabilities:
    def __init__(self):
        self.has_joystick = True

hardware_pinout = HardwarePinout()
