from machine import Pin


class HardwarePinout:
    class PinoutLEDS:
        def __init__(self):
            self.pin = Pin(12, Pin.OUT)

    class PinoutI2C:
        def __init__(self):
            self.pin_scl = Pin(18, Pin.OUT)
            self.pin_sda = Pin(9, Pin.OUT)

    class PinoutSPI:
        def __init__(self):
            self.pin_mosi = 6
            self.pin_miso = 8
            self.pin_sck = 7

    class PinoutDisplay:
        def __init__(self):
            self.pin_rst = 48
            self.pin_dc = 4
            self.pin_cs = 5

    def __init__(self):
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_i2c = self.PinoutI2C()
        self.pinout_spi = self.PinoutSPI()
        self.pinout_display = self.PinoutDisplay()


hardware_pinout = HardwarePinout()
