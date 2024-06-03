from machine import Pin


class HardwarePinout:
    class PinoutLEDS:
        def __init__(self):
            self.pin = Pin(12, Pin.OUT)

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

    class PinoutSAO:
        def __init__(self, leds: PinoutLEDS):
            self.gpio1 = leds.pin
            self.gpio2 = 13

    class PinoutSdCard:
        def __init__(self, spi: PinoutSPI):
            self.pin_mosi = spi.pin_mosi
            self.pin_miso = spi.pin_miso
            self.pin_sck = spi.pin_sck
            self.pin_cs = Pin(14)
            
    def __init__(self):
            self.pinout_leds = self.PinoutLEDS()
            self.pinout_spi = self.PinoutSPI()
            self.pinout_display = self.PinoutDisplay()
            self.pinout_sao = self.PinoutSAO(self.pinout_leds)
            self.pinout_sd_card = self.PinoutSdCard(self.pinout_spi)


hardware_pinout = HardwarePinout()
