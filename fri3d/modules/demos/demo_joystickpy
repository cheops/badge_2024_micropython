import time

from fri3d.badge import joystick


if __name__ == "__main__":

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
        print("increase analog joystick dead_val")
        joystick['x'].dead_val = 300
        joystick['y'].dead_val = 300
        j_x = joystick['x'].read()
        j_y = joystick['y'].read()
        print(f"{j_x=}, {j_y=}")

        # detect RIGHT, LEFT, UP, DOWN
        print("detect RIGHT, LEFT, UP, DOWN")
        directions = []
        j_x = joystick['x'].read()
        if j_x > 0:
            directions.append('RIGHT')
        if j_x < 0:
            directions.append('LEFT')

        j_y = joystick['y'].read()
        if j_y > 0:
            directions.append('UP')
        if j_y < 0:
            directions.append('DOWN')
        
        print(f"{directions=}")


        print("detect 10 joystick changes")
        prev_values = None
        changes = 0
        while changes < 10:

            values = {}

            values['j_x'] = joystick['x'].read()
            values['j_y'] = joystick['y'].read()

            print(f"{values}")
            time.sleep(0.1)

            if values != prev_values:
                changes += 1
                prev_values = values


