import time

from fonts.bitmap import vga1_16x16 as font
from fri3d.badge import leds, display, colors


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


print("Boot complete, starting application")
demo(leds)

sleeptime = 0.5

display.fill(colors.RED)
display.show()
time.sleep(sleeptime)

display.fill(colors.GREEN)
display.show()
time.sleep(sleeptime)

display.fill(colors.BLUE)
display.show()
time.sleep(sleeptime)

display.fill(colors.YELLOW)
display.show()
time.sleep(sleeptime)

display.fill(colors.BLACK)
display.show()
time.sleep(sleeptime)


def center(text):
    length = 1 if isinstance(text, int) else len(text)
    display.text(
        font,
        text,
        display.width() // 2 - length // 2 * font.WIDTH,
        display.height() // 2 - font.HEIGHT // 2,
    )
    display.show()


center("REPL")
