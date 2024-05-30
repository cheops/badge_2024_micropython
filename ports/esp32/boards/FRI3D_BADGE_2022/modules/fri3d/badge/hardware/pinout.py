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
                'boot': Pin(0, Pin.IN)   # has external pullup
            }

    class PinoutSAO:
        def __init__(self, leds: PinoutLEDS):
            self.gpio1 = leds.pin
            self.gpio2 = const(13)

    class PinoutGameon:
        def __init__(self):
            self.pin_buttons = {
                'a': Pin(13, Pin.IN, Pin.PULL_UP),
                'b': Pin(12, Pin.IN, Pin.PULL_UP),
                'start': Pin(32, Pin.IN, Pin.PULL_UP),
                'b': Pin(12, Pin.IN, Pin.PULL_UP),
                'b': Pin(12, Pin.IN, Pin.PULL_UP),
                'b': Pin(12, Pin.IN, Pin.PULL_UP),
                'b': Pin(12, Pin.IN, Pin.PULL_UP),
                'b': Pin(12, Pin.IN, Pin.PULL_UP),
                'b': Pin(12, Pin.IN, Pin.PULL_UP),
                'b': Pin(12, Pin.IN, Pin.PULL_UP),
            }            

    def __init__(self):
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_spi = self.PinoutSPI()
        self.pinout_display = self.PinoutDisplay()
        self.pinout_buttons = self.PinoutButtons()
        self.pinout_sao = self.PinoutSAO(self.pinout_leds)
        self.pinout_gameon = self.PinoutGameon()

hardware_pinout = HardwarePinout()
