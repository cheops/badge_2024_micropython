import s3lcd

from fri3d.badge.hardware import hardware_display

from .spi import spi

display = s3lcd.ESPLCD(
        bus=spi,
        width=hardware_display.width,
        height=hardware_display.height,
        inversion_mode=hardware_display.inversion,
        color_space=s3lcd.BGR,
        reset=hardware_display.pinout.pin_rst,
        rotation=hardware_display.rotation,
        rotations=hardware_display.rotations,
        dma_rows=48
    )

display.init()
