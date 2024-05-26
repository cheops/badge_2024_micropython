import lvgl as lv
from fri3d import logging

import fri3d.screens.wifi_conf
import fri3d.screens.ota_update

log = logging.Log(__name__, level=logging.DEBUG)

class ButtonLabel:
    def __init__(self, screen, label, cb):
        btn = lv.button(screen)
        self.btn = btn
        btn.set_height(30)
        lbl = lv.label(btn)
        lbl.set_text(label)
        lbl.align(lv.ALIGN.CENTER, 0, 0)
        btn.add_event_cb(self._bt_event_cb, lv.EVENT.CLICKED, None)
        self.cb = cb
    
    def _bt_event_cb(self, event):
        # code = event.get_code()
        self.cb()

class HomeScreen:
    def __init__(self):
        self._screen = lv.obj()
        self._construct()

    def load(self):
        lv.screen_load(self._screen)

    def _construct(self):
        screen = self._screen

        screen.set_style_bg_color(lv.palette_darken(lv.PALETTE.GREY, 4), lv.PART.MAIN)

        label = lv.label(screen)
        label.set_text("Hello world from MicroPython")
        label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        label.align(lv.ALIGN.CENTER, 0, 0)

        a = lv.anim_t()
        self.a = a
        a.init()
        a.set_var(label)
        a.set_values(10, 50)
        a.set_duration(1000)
        a.set_playback_delay(100)
        a.set_playback_duration(300)
        a.set_repeat_delay(500)
        a.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        a.set_path_cb(lv.anim_t.path_ease_in_out)
        a.set_custom_exec_cb(lambda _, v: label.set_y(v))
        a.start()
        
        def click_wifi():
            log.debug("clicked wifi")
            wifi_screen = fri3d.screens.wifi_conf.WifiScreen()
            wifi_screen.load()

        def click_ota_update():
            log.debug("clicked ota_update")
            ota_update_screen = fri3d.screens.ota_update.OtaUpdateScreen()
            ota_update_screen.load()


        btn = ButtonLabel(screen, lv.SYMBOL.WIFI + " wifi config", click_wifi)
        btn.btn.align(lv.ALIGN.CENTER, -80, -40)

        btn = ButtonLabel(screen, lv.SYMBOL.REFRESH + " ota update", click_ota_update)
        btn.btn.align(lv.ALIGN.CENTER, 80, -40)
