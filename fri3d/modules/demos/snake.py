import random
random.seed()

from collections import OrderedDict
from time import sleep_ms

from fri3d.badge import display, colors, buzzer
from fonts.bitmap import vga1_16x16 as font16
from fri3d.rtttl_player import play_rtttl

creeds_push_up_s = 'Creeds - Push Up:d=8,o=5,b=160:b,b,b,g,a,a,a,g,f#,f#,f#,f#,2f#'
game_over_song = 'GameOver:d=4,o=6,b=120:16c7,16b,16a,16g,16f,16e,4c'

eat_sound = 'Eat:d=4,o=5,b=120:8a#'


BUTTON_A_PIN = const(39)
BUTTON_B_PIN = const(40)
BUTTON_X_PIN = const(38)
BUTTON_Y_PIN = const(41)
BUTTON_MENU_PIN = const(45)
BUTTON_START_PIN = const(0)

class DebouncedButton:
    """
    Debounced pin handler

    - example usage with callback
    ```
        def button_pressed(btn:str):
            print(f"Button {btn} pressed.")
        db_y = DebouncedButton(Pin(BUTTON_Y_PIN, Pin.IN, Pin.PULL_UP), button_pressed, "Y")
    ```
    when button Y is pressed, the function button_pressed will get the argument "Y"

    - example usage to query the debounced value
    'db_y.value()' will return 1 when button Y is pressed down
    
    """

    def __init__(self, pin, cb=None, arg=None, debounce=200):
        self._pin = pin
        self.cb = cb
        self.arg = arg
        self.debounce = debounce
        self._start = time.ticks_ms()
        self._state = 0               # holds the current button state (1 = pressed)
        self._deb_passed = True       # temp var to check of debounce time has expired
        self._value = 1               # temp var to buffer pin.value()

        pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.debounce_handler)
    
    def value(self):
        self._deb_passed = time.ticks_diff(time.ticks_ms(), self._start) > self.debounce
        if self._state == 1 and self._deb_passed:
            self._value == self._pin.value()
            if self._value == 1:
                self._state = 0
        return self._state

    def set_callback_arg(cb=None, arg=None):
        self.cb = cb
        self.arg = arg

    def debounce_handler(self, pin):
        """debounce the pin"""
        self._value = pin.value()
        self._deb_passed = time.ticks_diff(time.ticks_ms(), self._start) > self.debounce
        
        if self._value == 0:
            # press
            if self._state == 0:
                self._state = 1
                self._start = time.ticks_ms()
                if not self.cb is None:
                    micropython.schedule(self.cb, self.arg)  # Schedule the function func to be executed “very soon”, outside irq
            else:
                # double trigger, ignore
                if self._deb_passed:
                    # we might have missed the up during debounce
                    self._start = time.ticks_ms()
                    if not self.cb is None:
                        micropython.schedule(self.cb, self.arg)  # Schedule the function func to be executed “very soon”, outside irq
        else:
            # release
            if self._deb_passed:
                self._state = 0


db_a = DebouncedButton(Pin(BUTTON_A_PIN, Pin.IN, Pin.PULL_UP))
db_b = DebouncedButton(Pin(BUTTON_B_PIN, Pin.IN, Pin.PULL_UP))
db_x = DebouncedButton(Pin(BUTTON_X_PIN, Pin.IN, Pin.PULL_UP))
db_y = DebouncedButton(Pin(BUTTON_Y_PIN, Pin.IN, Pin.PULL_UP))
db_menu = DebouncedButton(Pin(BUTTON_MENU_PIN, Pin.IN, Pin.PULL_UP))
db_start = DebouncedButton(Pin(BUTTON_START_PIN, Pin.IN))


mice = dict()
mousecount = 0
score = 0
mouse_amount = 4


def read_joystick():
    data = {
        'menu_click': db_menu.value(),
        'start_click': db_start.value(),
        'joy_cw': db_a.value(),
        'joy_ccw': db_b.value()
    }
    return data


def beep(beeplen):
    buzzer.freq(440)
    buzzer.duty(50)
    sleep_ms(beeplen)
    buzzer.duty(0)


def draw(y, x):
    display.pixel(x, y, colors.GREEN)


def game_over():
    global score
    display.fill(colors.BLACK)
    
    update_score(score)

    display.text(font16, 'MENU', 8, 40, colors.RED)
    display.text(font16, 'to exit', 8+6*16, 40, colors.WHITE)

    display.text(font16, 'Game Over', 70, 100, colors.WHITE)

    display.text(font16, 'START', 8, 160, colors.RED)
    display.text(font16, 'for new game', 8+6*16, 160, colors.WHITE)
    display.show()

    play_rtttl(game_over_song)

    score = 0


def update_score(score):
    display.text(font16, "score:", 80, 0, colors.YELLOW)
    display.text(font16, str(score), 80 + 7*16, 0)


def draw_mouse(x, y, mousenr, size=4):
    global mice
    global mousecount
    draw_y = y
    for i_y in range(size):
        draw_x = x
        for i_x in range(size):
            mouse_x, mouse_y = draw_x + i_x, draw_y + i_y
            display.pixel(mouse_x, mouse_y, colors.WHITE)
            mice[(mouse_x, mouse_y)] = mousenr
    mousecount += 1


x_min = 28 + 1
x_width = 240 -2
x_max = x_min + x_width
y_min = 17 + 1
y_height = 214 -2
y_max = y_min + y_height


def generate_mice(amount=3):
    global mice
    global score
    offset = max(mice.values()) if mice else 0
    for mousenr in range(1, amount):
        if score < 100:
            max_size = 4
        elif score < 250:
            max_size = 6
        elif score < 1000:
            max_size = 8
        elif score < 2000:
            max_size = 10
        else:
            max_size = 12
        size = random.randint(4, max_size)
        x_rand = random.randint(x_min + size, x_width - size)
        y_rand = random.randint(y_min + size, y_height - size)
        draw_mouse(x_rand, y_rand, offset + mousenr, size=size)
    display.show()



def start_game():
    beep(100)

    global mice
    global mousecount
    global score
    global mouse_amount
    display.fill(colors.BLACK)
    display.rect(x_min - 1, y_min - 1, x_width + 2, y_height + 2, colors.RED)
    display.show()
    grid = OrderedDict()
    snakelen = 15
    y = 32
    x = 64
    direction = 0
    prevscore = -1
    prevdata = read_joystick()
    generate_mice(3)
    while True:
        generate_mice(mouse_amount - mousecount)
        # snake hit itself
        if grid.get((x, y)):
            return

        # hit mouse
        mouse_nr = mice.get((x, y))
        if mouse_nr:
            mouse_blocks = []
            for mousexy, mousenr in mice.items():
                if mousenr == mouse_nr:
                    mouse_blocks.append(mousexy)
            for mousexy in mouse_blocks:
                del mice[mousexy]
                mouse_x, mouse_y = mousexy
                display.pixel(mouse_x, mouse_y, 0)
                score += 1
            display.show()
            mouse_amount = random.randint(3, 5)
            mousecount -= 1
            play_rtttl(eat_sound)
            snakelen += 5

        grid[(x, y)] = 1
        while len(grid) > snakelen:
            snaketail_k, snaketail_v = list(grid.items())[0]
            snaketail_x, snaketail_y = snaketail_k
            display.pixel(snaketail_x, snaketail_y, colors.BLACK)
            del grid[(snaketail_x, snaketail_y)]

        draw(y, x)

        data = read_joystick()
        if data['menu_click'] and not prevdata['menu_click']:
            return
        if data['joy_cw'] and not prevdata['joy_cw']:
            direction += 1
        if data['joy_ccw'] and not prevdata['joy_ccw']:
            direction -= 1
        
        if x >= x_max:
            x = x_min
        elif x <= x_min:
            x = x_max
        if y >= y_max:
            y = y_min
        elif y <= y_min:
            y = y_max

        if direction >= 4:
            direction = 0
        if direction < 0:
            direction = 3
        
        if direction == 0:
            x += 1
        if direction == 1:
            y += 1
        if direction == 2:
            x -= 1
        if direction == 3:
            y -= 1
        if score != prevscore:
            update_score(score)
        prevdata = data
        prevscore = score
        display.show()

def intro():
    display.fill(colors.BLACK)
    display.text(font16, 'SNAKE', 110, 40, colors.YELLOW)

    display.text(font16, 'A', 18, 80, colors.RED)
    display.text(font16, 'or', 18 + 2*16, 80, colors.WHITE)
    display.text(font16, 'B', 18 + 6*16, 80, colors.RED)
    display.text(font16, 'to turn', 18+8*16, 80, colors.WHITE)

    display.text(font16, 'MENU', 18, 120, colors.RED)
    display.text(font16, 'to exit', 18 + 5*16, 120, colors.WHITE)

    display.show()

    play_rtttl(creeds_push_up_s)

    display.text(font16, 'START', 8, 160, colors.RED)
    display.text(font16, 'for new game', 8+6*16, 160, colors.WHITE)
    display.show()

    while True:
        data = read_joystick()
        if data['start_click']:
            return True
        if data['menu_click']:
            return False

def outro():
    display.fill(colors.BLACK)
    display.text(font16, 'SNAKE', 110, 40, colors.YELLOW)
    display.text(font16, 'Thanks', 100, 80, colors.WHITE)
    display.text(font16, 'for playing', 60, 110, colors.WHITE)
    display.show()

    play_rtttl(creeds_push_up_s)

    display.fill(colors.BLACK)
    display.show()


def main():
    while True:
        start_game()
        game_over()
        while True:
            data = read_joystick()
            if data['start_click']:
                break
            if data['menu_click']:
                return

if __name__ == "__main__":
    start = intro()
    if start:
        main()
    outro()
