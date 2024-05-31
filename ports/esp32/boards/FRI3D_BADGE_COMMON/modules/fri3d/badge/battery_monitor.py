from machine import ADC

from fri3d.badge.hardware import hardware_battery_monitor

battery_monitor = ADC(hardware_battery_monitor.pinout.pin_battery_monitor, atten=ADC.ATTN_11DB)

