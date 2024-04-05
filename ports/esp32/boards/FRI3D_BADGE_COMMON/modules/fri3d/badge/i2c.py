import machine

from fri3d.badge.hardware import hardware_i2c

i2c = machine.I2C(
    scl=hardware_i2c.pinout.pin_scl,
    sda=hardware_i2c.pinout.pin_sda
)
