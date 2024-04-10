import s3lcd

from fri3d.badge.hardware import hardware_spi
from fri3d.badge.hardware import hardware_display

spi = s3lcd.SPI_BUS(
    spi_host=hardware_spi.id,
    sck=hardware_spi.pinout.pin_sck,
    mosi=hardware_spi.pinout.pin_mosi,
    dc=hardware_display.pinout.pin_dc,
    cs=hardware_display.pinout.pin_cs,
    pclk=hardware_spi.baudrate,
    
    #miso=hardware_spi.pinout.pin_miso,
    
    swap_color_bytes=True
)
