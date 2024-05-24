import machine
import os

from fri3d.badge.hardware import hardware_sd_card

sd = machine.SDCard(
    slot=hardware_sd_card.slot,
    sck=hardware_sd_card.pinout.pin_sck,
    mosi=hardware_sd_card.pinout.pin_mosi,
    miso=hardware_sd_card.pinout.pin_miso,
    cs=hardware_sd_card.pinout.pin_cs
)

sd_mounted = False

try:
    os.mount(sd, hardware_sd_card.mount_point)
    sd_mounted = True

except Exception as e:
    pass
