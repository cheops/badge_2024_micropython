from fri3d.badge.hardware import hardware_accelero

from .i2c import i2c

from wsen_isds import Wsen_Isds

wsen_isds = WSEN_ISDS(i2c=i2c, address=hardware_accelero.address)

class Accelero:
    def __init__(self, wsen_isds):
        self.wsen_isds = wsen_isds
        
    @property
    def acceleration(self):
        # TODO check if data is available
        return self.wsen_isds.read_accelerations()

accelero = Accelero(wsen_isds)
