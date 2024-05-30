joystick = {}

try:
    from fri3d.badge.hardware import hardware_joystick

    from .joystick_axis import JoystickAxis

    joystick['x'] = JoystickAxis(hardware_joystick.pinout.pin_joystick_x, dead_val=150)
    joystick['x'].init()

    joystick['y'] = JoystickAxis(hardware_joystick.pinout.pin_joystick_y, dead_val=150)
    joystick['y'].init()

except ImportError:
    pass