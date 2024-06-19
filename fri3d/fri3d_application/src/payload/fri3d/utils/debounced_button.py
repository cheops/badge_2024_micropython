import micropython
import time

from machine import Pin


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

        # Create references to bound methods beforehand
        # http://docs.micropython.org/en/latest/pyboard/library/micropython.html#micropython.schedule
        self._deb_handler = self.debounce_handler

        pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._deb_handler)
    
    def value(self):
        "return the debounced button value (1 if pressed, 0 otherwise)"
        self._deb_passed = time.ticks_diff(time.ticks_ms(), self._start_ms) > self.deb_ms
        if self._state == 1 and self._deb_passed:
            self._value == self._pin.value()
            if self._value == 1:
                self._state = 0
        return self._state

    def set_callback_arg(self, cb=None, arg=None):
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
                if self.cb is not None:
                    micropython.schedule(self.cb, self.arg)  # Schedule the function func to be executed “very soon”, outside irq
            else:
                # double trigger, ignore
                if self._deb_passed:
                    # we might have missed the up during debounce
                    self._start_ms = time.ticks_ms()
                    if self.cb is not None:
                        micropython.schedule(self.cb, self.arg)  # Schedule the function func to be executed “very soon”, outside irq
        else:
            # release
            if self._deb_passed:
                self._state = 0
