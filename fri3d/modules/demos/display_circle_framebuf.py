from micropython import const
from fri3d.badge import display, colors, spi
from fri3d import logging
from math import sin, cos, radians
import framebuf
import gc

log = logging.Log(__name__, level=logging.DEBUG)

log.debug("import done")



def cdj_logo_render():
    log.debug("starting")

    # fill the whole display with yellow, so that the left and right part have a color
    display.fill(colors.YELLOW)

    # bitmaps with character "0", "1"
    _SPRITE_WIDTH = const(24)
    _SPRITE_HEIGHT = const(40)
    SPRITE_BITMAPS = [
        bytearray([
            0b00111111, 0b11111111, 0b11111100,
            0b01111111, 0b11111111, 0b11111110,
            0b11111111, 0b11111111, 0b11111111,
            0b11111111, 0b11111111, 0b11111111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11110000, 0b00000000, 0b00001111,
            0b11111111, 0b11111111, 0b11111111,
            0b11111111, 0b11111111, 0b11111111,
            0b01111111, 0b11111111, 0b11111110,
            0b00111111, 0b11111111, 0b11111100
        ]),
        bytearray([
            0b01111111, 0b11111111, 0b00000000,
            0b11111111, 0b11111111, 0b00000000,
            0b11111111, 0b11111111, 0b00000000,
            0b01111111, 0b11111111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000000,
            0b00000000, 0b00001111, 0b00000110,
            0b00000000, 0b00001111, 0b00001111,
            0b00000000, 0b00001111, 0b00001111,
            0b00000000, 0b00001111, 0b00001111,
            0b00000000, 0b00001111, 0b00001111,
            0b00000000, 0b00001111, 0b00001111,
            0b00000000, 0b00001111, 0b00001111,
            0b00000000, 0b00001111, 0b00001111,
            0b01111111, 0b11111111, 0b11111111,
            0b11111111, 0b11111111, 0b11111111,
            0b11111111, 0b11111111, 0b11111111,
            0b01111111, 0b11111111, 0b11111111
        ])
    ]

    # create monochrome horizontal oriented framebuffers from the SPRITE_BITMAPS
    fbuf_0 = framebuf.FrameBuffer(SPRITE_BITMAPS[0], _SPRITE_WIDTH, _SPRITE_HEIGHT, framebuf.MONO_HLSB)
    fbuf_1 = framebuf.FrameBuffer(SPRITE_BITMAPS[1], _SPRITE_WIDTH, _SPRITE_HEIGHT, framebuf.MONO_HLSB)

    # create color mapping from the 2 bits to RBG565: white-black and black-white
    p_wb = bytearray([0x00, 0x00, 0xff, 0xff])
    fbuf_wb = framebuf.FrameBuffer(p_wb, 2, 1, framebuf.RGB565)
    p_bw = bytearray([0xff, 0xff, 0x00, 0x00])
    fbuf_bw = framebuf.FrameBuffer(p_bw, 2, 1, framebuf.RGB565)


    # we create a framebuffer of square size 240*240 and blit it at the center of the display
    # 2 circles move their center point on an imaginary circle with center k=120, h=120, r=60
    # move a point on a circle, 1 degree at a time
    # https://nl.wikipedia.org/wiki/Sinus_en_cosinus
    # sides of triangle: a = horizontal = x, b = vertical = y, c = slope = r
    _start_degrees = const(90)
    _step_degrees = const(1)
    _k = const(120)
    _h = const(120)
    _r = const(60)

    _width = const(240)
    _height = const(240)

    gc.collect()

    # FrameBuffer needs 2 bytes for every RGB565 pixel
    buff = bytearray(_width * _height * 2)
    fbuf = framebuf.FrameBuffer(buff, _width, _height, framebuf.RGB565)

    log.debug("framebuffer created")

    fbuf.fill(colors.YELLOW)  # fill with yellow

    display.blit_buffer(buff, 28, 0, _width, _height)


    # draw black outer circle 10 pixels wide, fill inner circle with yellow
    _outer_c_w = const(10)
    _outer_c_r = _r * 2


    fbuf.ellipse(_k, _h, _outer_c_r, _outer_c_r, 0x0000, True)
    display.blit_buffer(buff, 28, 0, _width, _height)
    display.show()

    #fbuf.ellipse(_k, _h, _outer_c_r - _outer_c_w, _outer_c_r - _outer_c_w, 0b1111111111100000, True)
    #display.blit_buffer(buff, 28, 0, _width, _height)
    #display.show()

    r_i = int(_r - (_outer_c_w / 2))
    h_s_w = int(_SPRITE_WIDTH / 2)

    log.debug("prep done")

    while True:

        log.debug("starting logo loop")
        gc.collect()

        for step in range(_start_degrees, _start_degrees + 360, _step_degrees):

            b = round(cos(radians(step)) * r_i)  # vertical
            a = round(sin(radians(step)) * r_i)  # horizontal

            x = _k - b
            y = _h - a

            x2 = _k + b
            y2 = _h + a

            # log.debug(step, a, b, x, y, x2, y2)

            # fbuf.pixel(x, y, colors.RED)
            fbuf.ellipse(x, y, r_i, r_i, 0xffff, True)
            # fbuf.text("0", x-4, y-4)
            fbuf.blit(fbuf_0, x - h_s_w, y - h_s_w, -1, fbuf_bw)

            # fbuf.pixel(x2, y2, colors.BLUE)
            fbuf.ellipse(x2, y2, r_i, r_i, 0x0000, True)
            # fbuf.text("1", x2-4, y2-4, 0xffff)
            fbuf.blit(fbuf_1, x2 - h_s_w, y2 - h_s_w, -1, fbuf_wb)

            display.blit_buffer(buff, 28, 0, _width, _height)

            display.show()
            # sleep_ms(30)





if __name__ == "__main__":
    cdj_logo_render()
