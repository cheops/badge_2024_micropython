from machine import I2C, Pin

from fri3d.badge.hardware import hardware_i2c


i2c = I2C(
    hardware_i2c.id,
    scl=Pin(hardware_i2c.pinout.scl),
    sda=Pin(hardware_i2c.pinout.sda),
    freq=hardware_i2c.freq,
)
