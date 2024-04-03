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
            self.pin_mosi = Pin(6, Pin.OUT)
            self.pin_miso = Pin(8, Pin.IN)
            self.pin_sck = Pin(7, Pin.OUT)

    class PinoutDisplay:
        def __init__(self):
            self.pin_rst = Pin(48, Pin.OUT)
            self.pin_dc = Pin(4, Pin.OUT)
            self.pin_cs = Pin(5, Pin.OUT)

    def __init__(self):
        self.pinout_leds = self.PinoutLEDS()
        self.pinout_i2c = self.PinoutI2C()
        self.pinout_spi = self.PinoutSPI()
        self.pinout_display = self.PinoutDisplay()


hardware_pinout = HardwarePinout()
