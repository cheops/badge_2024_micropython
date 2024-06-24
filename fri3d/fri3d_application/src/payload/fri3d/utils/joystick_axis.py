from machine import ADC


class JoystickAxis:
    """one axis of an analog joystick
       pin_nr: pin that the analog joystick is connected to
       dead_val: what is the value to still be considered in the dead center (default 5)
       center: what is the value of the center (default 3.3 Volt / 2 * 1000 = 1650)
               you can also use calibrate_center()
    """
    def __init__(self, pin_nr: int, dead_val=5, center=1650):
        self._pin_nr = pin_nr
        self.dead_val = dead_val
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
            # log.debug(f"calibrate raw_val: {r}")
            sum += r // 1000
        self._center = sum // 10
        # log.debug(f"calibrate result: {self._center - 1650}")
        return self._center - 1650

    def read(self):
        "returns a value between -1650 and +1650 if center is in the middle, corresponds to mV"
        uv_val = self._adc.read_uv()  # read_uv() uses the known characteristics of the ADC and per-package eFuse values
        uv_val = uv_val // 1000
        uv_val = uv_val - self._center
        if -self.dead_val < uv_val and uv_val < self.dead_val:
            uv_val = 0
        return uv_val
