from machine import Pin


class HardwarePinout:
    class PinoutLEDS:
        def __init__(self):
            self.pin = Pin(2, Pin.OUT)

    class PinoutSPI:
        def __init__(self):
            self.pin_mosi = 23
            self.pin_miso = 19
            self.pin_sck = 18

    class PinoutDisplay:
        def __init__(self):
            self.pin_rst = 32
            self.pin_dc = 33
            self.pin_cs = 5

    class PinoutSAO:
        def __init__(self, leds: PinoutLEDS):
            self.gpio1 = leds.pin
            self.gpio2 = 13

    def __init__(self):
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_spi = self.PinoutSPI()
        self.pinout_display = self.PinoutDisplay()
        self.pinout_sao = self.PinoutSAO(self.pinout_leds)


hardware_pinout = HardwarePinout()
