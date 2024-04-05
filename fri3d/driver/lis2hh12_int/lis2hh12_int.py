import lis2hh12.py

# extra functionality look at
# https://github.com/tinypico/tinypico-micropython/tree/master/lis3dh%20library

class LIS2HH12_int(lis2hh12.LIS2HH12):
    def enable_act_int(self):
        self._register_char(_CTRL6, 0x0A)
