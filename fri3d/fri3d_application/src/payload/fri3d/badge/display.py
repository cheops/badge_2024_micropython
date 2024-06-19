from lvgl_esp32 import Display

from fri3d.badge.hardware import hardware_display

from .spi import spi

display = Display(
    spi=spi,
    width=hardware_display.width,
    height=hardware_display.height,
    swap_xy=hardware_display.swap_xy,
    mirror_x=hardware_display.mirror_x,
    mirror_y=hardware_display.mirror_y,
    invert=hardware_display.invert,
    bgr=hardware_display.bgr,
    reset=hardware_display.pinout.pin_rst,
    dc=hardware_display.pinout.pin_dc,
    cs=hardware_display.pinout.pin_cs,
    pixel_clock=hardware_display.pixel_clock,
)

display.init()
