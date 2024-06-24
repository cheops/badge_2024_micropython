from machine import Pin

from fri3d.badge.hardware import hardware_capabilities
from fri3d.utils.debounced_button import DebouncedButton


class Buttons:
    def _init_buttons(self, b):
        for button in b.buttons:
            p = getattr(b.pinout, f"pin_{button}")

            setattr(
                self,
                button,
                DebouncedButton(Pin(
                    p.pin,
                    Pin.IN,
                    Pin.PULL_UP if p.pull_up else None,
                )),
            )

    def __init__(self):
        # Initialize all the possible buttons to None
        self.a = None
        self.b = None
        self.x = None
        self.y = None
        self.menu = None
        self.start = None
        self.boot = None
        self.select = None
        self.p0 = None
        self.p1 = None
        self.up = None
        self.left = None
        self.down = None
        self.right = None
        self.p3 = None

        # Generic buttons that can be mapped to other buttons
        self.previous = None
        self.next = None
        self.confirm = None
        self.escape = None
        self.home = None
        self.end = None

        if hardware_capabilities.onboard_buttons:
            from fri3d.badge.hardware import hardware_onboard_buttons
            self._init_buttons(hardware_onboard_buttons)

        # TODO: Make this configurable whether the GameOn is plugged in or not
        if hardware_capabilities.game_on:
            from fri3d.badge.hardware import hardware_gameon
            self._init_buttons(hardware_gameon.buttons)

        if self.y:
            self.previous = self.y
        elif self.p0:
            self.previous = self.p0

        if self.x:
            self.next = self.x
        elif self.p1:
            self.next = self.p1

        if self.a:
            self.confirm = self.a

        if self.b:
            self.escape = self.b

        if self.menu:
            self.home = self.menu
        elif self.select:
            self.home = self.select

        if self.start:
            self.end = self.start

buttons = Buttons()
