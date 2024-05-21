from machine import Pin, ADC
from micropython import const
import micropython
import time

from fri3d import logging

log = logging.Log(__name__, level=logging.DEBUG)

JOY_X = const(1)
JOY_Y = const(3)

BUTTON_A_PIN = const(39)
BUTTON_B_PIN = const(40)
BUTTON_X_PIN = const(38)
BUTTON_Y_PIN = const(41)
BUTTON_MENU_PIN = const(45)
BUTTON_START_PIN = const(0)


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


class DebouncedButton:
    """
    Debounced pin handler

    - example usage with callback
    ```
        def button_pressed(btn:str):
            print(f"Button {btn} pressed.")
        db_y = DebouncedButton(Pin(BUTTON_Y_PIN, Pin.IN, Pin.PULL_UP), button_pressed, "Y")
    ```
    when button Y is pressed, the function button_pressed will get the argument "Y"

    - example usage to query the debounced value
    'db_y.value()' will return 1 when button Y is pressed down

    Parameters:
    pin (machine.Pin): initialized machine.Pin instance
    cb (function): callback function that will be called when button is pressed (outside irq)
    arg: arguments to be supplied to the cb function
    debounce_ms (int): debounce time in ms, default 200 ms
    """

    def __init__(self, pin, cb=None, arg=None, debounce_ms=200):
        self._pin = pin
        self.cb = cb
        self.arg = arg
        self.deb_ms = debounce_ms
        self._start_ms = time.ticks_ms()
        self._state = 0               # holds the current button state (1 = pressed)
        self._deb_passed = True       # temp var to check if debounce time has expired
        self._value = 1               # temp var to buffer pin.value()

        pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.debounce_handler)
    
    def value(self):
        "return the debounced button value (1 if pressed, 0 otherwise)"
        self._deb_passed = time.ticks_diff(time.ticks_ms(), self._start_ms) > self.deb_ms
        if self._state == 1 and self._deb_passed:
            self._value == self._pin.value()
            if self._value == 1:
                self._state = 0
        return self._state

    def set_callback_arg(cb=None, arg=None):
        self.cb = cb
        self.arg = arg

    def debounce_handler(self, pin):
        """debounce the pin"""
        self._value = pin.value()
        self._deb_passed = time.ticks_diff(time.ticks_ms(), self._start_ms) > self.deb_ms
        
        if self._value == 0:
            # press
            if self._state == 0:
                self._state = 1
                self._start_ms = time.ticks_ms()
                if not self.cb is None:
                    micropython.schedule(self.cb, self.arg)  # Schedule the function func to be executed “very soon”, outside irq
            else:
                # double trigger, ignore
                if self._deb_passed:
                    # we might have missed the up during debounce
                    self._start_ms = time.ticks_ms()
                    if not self.cb is None:
                        micropython.schedule(self.cb, self.arg)  # Schedule the function func to be executed “very soon”, outside irq
        else:
            # release
            if self._deb_passed:
                self._state = 0


joy_x = JoyStick(JOY_X)
joy_x.init()

joy_y = JoyStick(JOY_Y)
joy_y.init()



but_A = DebouncedButton(Pin(BUTTON_A_PIN, Pin.IN, Pin.PULL_UP))
but_B = DebouncedButton(Pin(BUTTON_B_PIN, Pin.IN, Pin.PULL_UP))
but_X = DebouncedButton(Pin(BUTTON_X_PIN, Pin.IN, Pin.PULL_UP))
but_Y = DebouncedButton(Pin(BUTTON_Y_PIN, Pin.IN, Pin.PULL_UP))
but_MENU = DebouncedButton(Pin(BUTTON_MENU_PIN, Pin.IN, Pin.PULL_UP))
but_START = DebouncedButton(Pin(BUTTON_START_PIN, Pin.IN))  # has external pullup


if __name__ == "__main__":

    try:
        c = joy_x.calibrate_center()
        print("x calibrate: ", c)

        c = joy_y.calibrate_center()
        print("y calibrate: ", c)

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

