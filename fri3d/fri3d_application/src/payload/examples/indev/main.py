import lvgl as lv
import lvgl_esp32

from fri3d.badge.display import display
from fri3d.indev.indev import Indev


class CounterBtn:
    def __init__(self, rel_y_pos):
        screen = lv.screen_active()

        screen.set_style_bg_color(lv.palette_darken(lv.PALETTE.GREY, 4), lv.PART.MAIN)

        self.btn = lv.button(screen)
        self.btn.align(lv.ALIGN.CENTER, 0, rel_y_pos)

        self.lbl = lv.label(self.btn)
        self.lbl.set_text("Button")

        self.cnt = 0

        self.btn.add_event_cb(self.btn_cb, lv.EVENT.ALL, None)

        # lv.screen_load(screen)

    def btn_cb(self, evt):
        code = evt.get_code()
        if code == lv.EVENT.CLICKED:
            self.cnt += 1
            print(self.cnt)

            self.lbl.set_text("Button: " + str(self.cnt))


wrapper = lvgl_esp32.Wrapper(display)
wrapper.init()

indev = Indev()

counter_btn1 = CounterBtn(-20)
counter_btn2 = CounterBtn(20)


# draw the buffers to the screen
while True:
    lv.timer_handler_run_in_period(5)
