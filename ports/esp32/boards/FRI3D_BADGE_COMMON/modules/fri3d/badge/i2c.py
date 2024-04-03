import machine

from fri3d.badge.hardware import hardware_i2c

i2c = machine.I2C(
    scl=hardware_ic2.pinout.pin_scl,
    sda=hardware_ic2.pinout.pin_sda
)
