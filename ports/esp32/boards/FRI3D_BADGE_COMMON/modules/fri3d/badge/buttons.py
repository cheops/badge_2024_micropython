from fri3d.badge.hardware import hardware_buttons

from .debounced_button import DebouncedButton

buttons = {}


for n, pin in hardware_buttons.pinout.pin_buttons.items():
    buttons[n] = DebouncedButton(pin)


try:
    from fri3d.badge.hardware import hardware_gameon

    for n, pin in hardware_gameon.pinout.pin_buttons.items():
        buttons[n] = DebouncedButton(pin)

except ImportError:
    pass
