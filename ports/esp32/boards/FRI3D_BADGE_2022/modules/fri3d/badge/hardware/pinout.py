from micropython import const
from machine import Pin


class HardwarePinout:
    class PinoutLEDS:
        def __init__(self):
            self.pin = Pin(2, Pin.OUT)

    class PinoutSPI:
        def __init__(self):
            self.pin_mosi = const(23)
            self.pin_miso = const(19)
            self.pin_sck = const(18)

    class PinoutDisplay:
        def __init__(self):
            self.pin_rst = const(32)
            self.pin_dc = const(33)
            self.pin_cs = const(5)

    class PinoutButtons:
        def __init__(self):
            self.pin_buttons = {
                'boot': Pin(0, Pin.IN)  # has external pullup
            }

    class PinoutSAO:
        def __init__(self, leds: PinoutLEDS):
            self.gpio1 = leds.pin
            self.gpio2 = const(13)

    class PinoutBatteryMonitor:
        def __init__(self):
            self.pin_battery_monitor = const(35)

    class PinoutGameon:
        def __init__(self):
            self.pin_buttons = {
                "a": Pin(13, Pin.IN, Pin.PULL_UP),
                "b": Pin(12, Pin.IN, Pin.PULL_UP),
                "start": Pin(32, Pin.IN, Pin.PULL_DOWN),  # is active high
                "select": Pin(36, Pin.IN, Pin.PULL_UP),
                "p0": Pin(27, Pin.IN, Pin.PULL_UP),
                "p1": Pin(14, Pin.IN, Pin.PULL_UP),
                "up": Pin(39, Pin.IN, Pin.PULL_UP),
                "left": Pin(26, Pin.IN, Pin.PULL_UP),
                "down": Pin(15, Pin.IN, Pin.PULL_UP),
                "right": Pin(0, Pin.IN),  # has external pullup
                "p3": Pin(34, Pin.IN, Pin.PULL_UP)
             }

    def __init__(self):
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_spi = self.PinoutSPI()
        self.pinout_display = self.PinoutDisplay()
        self.pinout_buttons = self.PinoutButtons()
        self.pinout_sao = self.PinoutSAO(self.pinout_leds)
        self.pinout_battery_monitor = self.PinoutBatteryMonitor()
        self.pinout_gameon = self.PinoutGameon()

hardware_pinout = HardwarePinout()
