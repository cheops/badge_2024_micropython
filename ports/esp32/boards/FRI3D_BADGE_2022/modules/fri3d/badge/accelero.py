from fri3d.badge.hardware import hardware_accelero

from .i2c import i2c

from lis2hh12_int import LIS2HH12_int

lis2hh12_int = LIS2HH12_int(i2c=i2c, address=hardware_accelero.address)


class Accelero:
    def __init__(self, lis2hh12_int):
        self.lis = lis2hh12_int
        
        self.lis.enable_act_int()

    @property
    def acceleration(self):
        return self.lis.acceleration()

accelero = Accelero(lis2hh12_int)
