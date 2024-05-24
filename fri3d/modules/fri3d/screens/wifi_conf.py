import lvgl as lv
from fri3d import logging

import fri3d.screens.home

log = logging.Log(__name__, level=logging.DEBUG)


class TextArea:
    def __init__(self, screen, kb):
        self.ta = lv.textarea(screen)
        self.ta.add_event_cb(self._ta_event_cb, lv.EVENT.ALL, None);
        self._kb = kb

    def _ta_event_cb(self, event):
        code = event.get_code()
        if code == lv.EVENT.CLICKED or code == lv.EVENT.FOCUSED:
            self._kb.set_textarea(self.ta)

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



class WifiScreen:
    def __init__(self):
        self._screen = lv.obj()
        self._construct()

    def load(self):
        lv.screen_load(self._screen)

    def _save_cb(self):
        ssid = self.ss_ta.ta.get_text()
        key = self.key_ta.ta.get_text()
        print(f"{ssid=}, {key=}")
        # TODO save
    
    def _cancel_cb(self):
        print("Cancel")
        home_screen = fri3d.screens.home.HomeScreen()
        home_screen.load()

    def _construct(self):
        screen = self._screen

        # title
        title = lv.label(screen)
        title.set_text("Wifi Configuration")
        title.align(lv.ALIGN.TOP_MID, 0, 0)

        # keyboard
        kb = lv.keyboard(screen)
        kb.set_size(screen.get_width(), int(screen.get_height()/2) )

        ss_ta = TextArea(screen, kb)
        self.ss_ta = ss_ta
        ss_ta.ta.set_text("")
        ss_ta.ta.set_one_line(True)
        ss_ta.ta.set_width(lv.pct(50))
        ss_ta.ta.set_pos(100, 20)

        # ssid label
        ss_lbl = lv.label(screen)
        ss_lbl.set_text("SSID:")
        ss_lbl.align_to(ss_ta.ta, lv.ALIGN.OUT_LEFT_MID, -5, 0)

        # key box
        key_ta = TextArea(screen, kb)
        self.key_ta = key_ta
        key_ta.ta.set_text("")
        key_ta.ta.set_password_mode(True)
        key_ta.ta.set_one_line(True)
        key_ta.ta.set_width(lv.pct(50))
        key_ta.ta.set_pos(100, 60)

        # key label
        key_lbl = lv.label(screen)
        key_lbl.set_text("Key:")
        key_lbl.align_to(key_ta.ta, lv.ALIGN.OUT_LEFT_MID, -5, 0)

        # focus the keyboard
        kb.set_textarea(ss_ta.ta)

        # save button
        sv = ButtonLabel(screen, "Save", self._save_cb)
        sv.btn.align(lv.ALIGN.RIGHT_MID, -5, -15)
        
        # cancel button
        cancel = ButtonLabel(screen, "Cancel", self._cancel_cb)
        cancel.btn.align(lv.ALIGN.LEFT_MID, 5, -15)




