from machine import UART

from fri3d.badge.hardware import hardware_uart


uart = UART(
    hardware_uart.id,
    rx=hardware_uart.pinout.rx,
    tx=hardware_uart.pinout.tx
)
