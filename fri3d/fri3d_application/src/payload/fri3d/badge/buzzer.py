from machine import PWM

from fri3d.badge.hardware import hardware_buzzer


buzzer = PWM(
    hardware_buzzer.pinout.pin_buzzer, 
    freq=hardware_buzzer.freq, 
    duty=hardware_buzzer.duty)