import machine

from fri3d.badge.hardware import hardware_i2c

i2c = machine.I2C(
    0,
    scl=machine.Pin(hardware_i2c.pinout.pin_scl),
    sda=machine.Pin(hardware_i2c.pinout.pin_sda)
)
