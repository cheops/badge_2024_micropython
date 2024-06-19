import time

from fri3d.badge.buttons import buttons

print("Waiting on button press A")
while buttons.a.value() == 0:
    time.sleep(0.1)

print("Button pressed!")
