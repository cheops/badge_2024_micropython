import lvgl as lv

from fri3d.badge import buttons
from fri3d.badge import joystick

from fri3d import logging

log = logging.Log(__name__, level=logging.DEBUG)

"""
    A             : LV_KEY_ENTER
    B             : LV_KEY_ESC
    X | P0        : LV_KEY_NEXT
    Y | P1        : LV_KEY_PREV

    MENU | SELECT : LV_KEY_HOME
    START         : LV_KEY_END

    JOY_UP        : LV_KEY_UP
    JOY_DOWN      : LV_KEY_DOWN
    JOY_LEFT      : LV_KEY_LEFT
    JOY_RIGHT     : LV_KEY_RIGHT
"""


if 'a' in buttons:
    button_enter = buttons['a']

if 'b' in buttons:
    button_esc = buttons['b']

if 'x' in buttons:
    button_next = buttons['x']
elif 'p0' in buttons:
    button_next = buttons['p0']

if 'y' in buttons:
    button_prev = buttons['y']
if 'p1' in buttons:
    button_prev = buttons['p1']

if 'menu' in buttons:
    button_home = buttons['menu']
elif 'select' in buttons:
    button_home = buttons['select']

if 'start' in buttons:
    button_end = buttons['start']

analog_joystick = True if 'x' in joystick and 'y' in joystick else False

# remember the last key pressed reported to lvgl
last_key_pressed = None

def read_buttons(drv, data):
    global last_key_pressed

    keys_pressed = []

    if button_enter.value():
        keys_pressed.append(lv.KEY.ENTER)
    if button_esc.value():
        keys_pressed.append(lv.KEY.ESC)
    if button_next.value():
        keys_pressed.append(lv.KEY.NEXT)
    if button_prev.value():
        keys_pressed.append(lv.KEY.PREV)
    if button_home.value():
        keys_pressed.append(lv.KEY.HOME)
    if button_end.value():
        keys_pressed.append(lv.KEY.END)

    if analog_joystick:
        j_x = joystick['x'].read()
        if j_x > 0:
            keys_pressed.append(lv.KEY.RIGHT)
        if j_x < 0:
            keys_pressed.append(lv.KEY.LEFT)

        j_y = joystick['y'].read()
        if j_y > 0:
            keys_pressed.append(lv.KEY.UP)
        if j_y < 0:
            keys_pressed.append(lv.KEY.DOWN)
    else:
        if buttons['up'].value():
            keys_pressed.append(lv.KEY.UP)
        if buttons['left'].value():
            keys_pressed.append(lv.KEY.LEFT)
        if buttons['down'].value():
            keys_pressed.append(lv.KEY.DOWN)
        if buttons['right'].value():
            keys_pressed.append(lv.KEY.RIGHT)


    if last_key_pressed is not None:
        if last_key_pressed not in keys_pressed:
            # last key released
            # log.debug(f"released {last_key_pressed}")

            data.key = last_key_pressed
            data.state = lv.INDEV_STATE.RELEASED
            last_key_pressed = None

            if keys_pressed:
                # another key is pressed
                data.continue_reading = True
            else:
                data.continue_reading = False
        else:
            # last key still pressed
            data.key = last_key_pressed
            data.state = lv.INDEV_STATE.PRESSED
            data.continue_reading = False
    else:
        if keys_pressed:
            # can only send 1 key pressed to lvgl, send first
            key_pressed = keys_pressed.pop(0)

            # log.debug(f"pressed {key_pressed}")

            data.key = key_pressed
            data.state = lv.INDEV_STATE.PRESSED
            data.continue_reading = False

            last_key_pressed = key_pressed
