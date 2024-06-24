from lvgl_esp32 import SPI

from fri3d.badge.hardware import hardware_spi

spi = SPI(
    hardware_spi.id,
    baudrate=hardware_spi.baudrate,
    sck=hardware_spi.pinout.pin_sck,
    mosi=hardware_spi.pinout.pin_mosi,
    miso=hardware_spi.pinout.pin_miso,
)

spi.init()
