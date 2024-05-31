import time

from fri3d import logging
from fri3d.power import Power

log = logging.Log(__name__, level=logging.DEBUG)

power = fri3d.power.Power()

while True:
    p = power.battery_percentage
    log.debug(f"battery_percentage: {p}")
    time.sleep(2)
