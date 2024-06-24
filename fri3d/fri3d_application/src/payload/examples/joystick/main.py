# Note that this example will not work with a GameOn as that doesn't have a real joystick but buttons!
import time

from fri3d.badge.joystick import joystick

previous_x = 0
previous_y = 0

print("Do not touch the joystick while we calibrate")
time.sleep(3)
joystick.x.calibrate_center()
joystick.y.calibrate_center()

print("Move the joystick")
while True:
    x = joystick.x.read()
    y = joystick.y.read()

    if x != previous_x or y != previous_y:
        print(f"({x}, {y})")

    time.sleep(0.1)
