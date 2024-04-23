from machine import Pin, Signal, ADC
from micropython import const
import time

from fri3d import logging

log = logging.Log(__name__, level=logging.DEBUG)

BUTTON_A_PIN = const(39)
BUTTON_B_PIN = const(40)
BUTTON_X_PIN = const(38)
BUTTON_Y_PIN = const(41)
BUTTON_MENU_PIN = const(45)
BUTTON_START_PIN = const(0)

JOY_X = const(1)
JOY_Y = const(3)

class JoyStick:
    """one axis of an analog joystick
       pin_nr: pin that the analog joystick is connected to
       dead_val: what is the value to still be considered in the dead center (default 5)
       center: what is the value of the center (default 3.3 Volt / 2 * 1000 = 1650)
               you can also use calibrate_center()
    """
    def __init__(self, pin_nr: int, dead_val=5, center=1650):
        self._pin_nr = pin_nr
        self._dead_val = dead_val
        self._center = center
    
    def init(self):
        "creates the ADC"
        self._adc = ADC(self._pin_nr, atten=ADC.ATTN_11DB)
    
    def deinit(self):
        "stops the ADC"
        del self._adc
    
    def read_uv(self):
        "return the ADC.read_uv value, uses the known characteristics of the ADC and per-package eFuse values"
        return self._adc.read_uv()
    
    def calibrate_center(self):
        "put the joystick in the middle, makes 10 readings and averages to the center point"
        sum = 0
        for _ in range(10):
            r = self._adc.read_uv()
            log.debug(f"calibrate raw_val: {r}")
            sum += r // 1000
        self._center = sum // 10
        log.debug(f"calibrate result: {self._center - 1650}")
        return self._center - 1650

    def read(self):
        "returns a value between -1650 and +1650 if center is in the middle, corresponds to mV"
        uv_val = self._adc.read_uv()  # read_uv() uses the known characteristics of the ADC and per-package eFuse values
        uv_val = uv_val // 1000
        uv_val = uv_val - self._center
        if -self._dead_val < uv_val and uv_val < self._dead_val:
            uv_val = 0
        return uv_val



joy_x = JoyStick(JOY_X)
joy_x.init()
c = joy_x.calibrate_center()
print("x calibrate: ", c)

joy_y = JoyStick(JOY_Y)
joy_y.init()
c = joy_y.calibrate_center()
print("y calibrate: ", c)

but_A = Signal(Pin(BUTTON_A_PIN, Pin.IN, Pin.PULL_UP), invert=True)
but_B = Signal(Pin(BUTTON_B_PIN, Pin.IN, Pin.PULL_UP), invert=True)
but_X = Signal(Pin(BUTTON_X_PIN, Pin.IN, Pin.PULL_UP), invert=True)
but_Y = Signal(Pin(BUTTON_Y_PIN, Pin.IN, Pin.PULL_UP), invert=True)
but_MENU = Signal(Pin(BUTTON_MENU_PIN, Pin.IN, Pin.PULL_UP), invert=True)
but_START = Signal(Pin(BUTTON_START_PIN, Pin.IN), invert=True)  # has external pullup


if __name__ == "__main__":

    try:
        for _ in range(100):
            j_x = joy_x.read()
            j_y = joy_y.read()
            a = but_A.value()
            b = but_B.value()
            x = but_X.value()
            y = but_Y.value()
            menu = but_MENU.value()
            start = but_START.value()

            print(f"{j_x=}, {j_y=}, {a=}, {b=}, {x=}, {y=}, {menu=}, {start=}")

            time.sleep(0.1)

    except KeyboardInterrupt:
        joy_x.deinit()
        joy_y.deinit()
        pass

