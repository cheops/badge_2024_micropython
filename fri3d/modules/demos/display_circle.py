from fri3d.badge import colors
from fri3d.badge import display
from fri3d import logging

from fonts.bitmap import vga1_16x16 as font16

from math import sin, cos, radians
from time import sleep_ms

log = logging.Log(__name__, level=logging.DEBUG)

log.debug("fill display BLACK")
display.fill(colors.BLACK)
display.show()
sleep_ms(30)

# circle center (x=h, y=k)
# ( x - h) * ( x- h ) + ( y - k ) * ( y - k ) = r * r


# 2 circles move their center point on an imaginary circle with center k=148, h=120, r=60
# move a point on a circle, 1 degree at a time
# https://nl.wikipedia.org/wiki/Sinus_en_cosinus
# sides of triangle: a = horizontal = x, b = vertical = y, c = slope = r
start_degrees = 270
step_degrees = 1
k=148
h=120
r=60

while True:
    log.debug("start loop")
    for steps in range(start_degrees, start_degrees + 360, step_degrees ):

        b = round( cos(radians(steps)) * r )
        a = round( sin(radians(steps)) * r )

        x = k - b
        y = h - a

        x2 = k + b
        y2 = h + a

        #log.debug(steps, a, b, x, y, x2, y2)

        #display.pixel(x, y, colors.RED)
        display.fill_circle(x, y, r, colors.WHITE)
        display.text(font16, "0", x, y, colors.BLACK, colors.WHITE)

        #display.pixel(x2, y2, colors.BLUE)
        display.fill_circle(x2, y2, r, colors.BLACK)
        display.text(font16, "1", x2, y2, colors.WHITE, colors.BLACK)
        display.show()

        #sleep_ms(30)



