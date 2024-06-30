from machine import I2S, Pin

from fri3d.badge.hardware import hardware_i2s

# TODO
i2s_out = I2S(
    hardware_i2s.id,
    sck=Pin(hardware_i2s.pinout.sck),
    ws=Pin(hardware_i2s.pinout.ws),
    sd=Pin(hardware_i2s.pinout.sd),
    mode=I2S.TX,
    bits=hardware_i2s.bits,
    format=I2S.MONO,
    rate=hardware_i2s.rate,
    ibuf=hardware_i2s.ibuf,
)

# TODO: audio input
