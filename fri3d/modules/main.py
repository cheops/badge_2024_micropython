import machine
import time
import lvgl_esp32
import lvgl as lv

from fri3d.badge.hardware import hardware_sao
from fri3d.badge import leds, display
from fri3d.buttons_indev import read_buttons
from fri3d import logging

import fri3d.screens.home

log = logging.Log(__name__, level=logging.DEBUG)

def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()


# Initialize the screen
wrapper = lvgl_esp32.Wrapper(display)
wrapper.init()

indev_drv = lv.indev_create()
indev_drv.set_type(lv.INDEV_TYPE.KEYPAD)
indev_drv.set_read_cb(read_buttons)
indev_drv.set_display(lv.display_get_default())
grp = lv.group_create()
grp.set_default()
indev_drv.set_group(grp)
indev_drv.enable(True)

# We check some inputs at boot to see if we need to boot in a special mode
repl_pin = machine.Pin(hardware_sao.pinout.gpio2, machine.Pin.IN, machine.Pin.PULL_UP)


if repl_pin.value() == 0:
    print("Detected REPL pin active, dropping into REPL")

else:
    print("Boot complete, starting application")
    demo(leds)

    home_screen = fri3d.screens.home.HomeScreen()
    home_screen.load()

    while True:
        lv.timer_handler_run_in_period(5)
