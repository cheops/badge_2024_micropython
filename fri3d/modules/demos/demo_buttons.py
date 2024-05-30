import time

from fri3d.badge import buttons
from fri3d.badge import joystick


if __name__ == "__main__":

    # read the actual debounced value from button
    print("read the actual debounced value from button")
    value_a = buttons['a'].value()
    print(value_a)
    
    value_b = buttons['b'].value()
    print(value_b)

    # add callback to button press
    print("add callback to button press")
    buttons['a'].set_callback_arg(lambda x: print(f"button pressed"))
    buttons['b'].set_callback_arg(lambda x: print(f"button pressed"))

    time.sleep(1)

    # add callback with args to button press
    print("add callback with args to button press")
    buttons['a'].set_callback_arg(lambda x: print(f"button {x} pressed"), 'a')
    buttons['b'].set_callback_arg(lambda x: print(f"button {x} pressed"), 'b')

    time.sleep(1)

    # add callback function with args to button press
    print("add callback function with args to button press")
    def button_callback(args):
        print(f"button {args} pressed")

    buttons['a'].set_callback_arg(button_callback, 'a')
    buttons['b'].set_callback_arg(button_callback, 'b')

    time.sleep(1)

    # add callback function with multiple args to button press
    print("add callback function with multiple args to button press")
    total_count = 0
    def button_callback(args):
        n, c = *args
        print(f"button {n} pressed, total_count: {c}")

    buttons['a'].set_callback_arg(button_callback, ('a', total_count))
    buttons['b'].set_callback_arg(button_callback, ('b', total_count))

    time.sleep(1)

    # remove callback from button press
    print("remove callback from button press")
    buttons['a'].set_callback_arg(None, None)
    buttons['b'].set_callback_arg(None, None)


    # analog joystick present?
    analog_joystick = True if 'x' in joystick and 'y' in joystick else False
    print(f"{analog_joystick=}")

    # read values from analog joystick
    if analog_joystick:
        print("read values from analog joystick")
        j_x = joystick['x'].read()
        j_y = joystick['y'].read()
        print(f"{j_x=}, {j_y=}")


    # calibrate analog joystick
    if analog_joystick:
        print("CALIBRATION: center the joystick, and do not touch it")
        time.sleep(1)

        c = joystick['x'].calibrate_center()
        print("x calibrate: ", c)

        c = joystick['y'].calibrate_center()
        print("y calibrate: ", c)

        j_x = joystick['x'].read()
        j_y = joystick['y'].read()
        print(f"{j_x=}, {j_y=}")

    # increase analog joystick dead_val
    if analog_joystick:
        print("increase analog joystick dead_val")
        joystick['x'].dead_val = 300
        joystick['y'].dead_val = 300
        j_x = joystick['x'].read()
        j_y = joystick['y'].read()
        print(f"{j_x=}, {j_y=}")


    print("detect 10 different button changes")
    prev_values = None
    changes = 0
    while changes < 10:

        values = {}

        for b in buttons:
            values[b] = buttons[b].value()

        if analog_joystick:
            values['j_x'] = joystick['x'].read()
            values['j_y'] = joystick['y'].read()

        print(f"{values}")
        time.sleep(0.1)

        if values != prev_values:
            changes += 1
            prev_values = values


