import lvgl as lv

from fri3d import logging

import fri3d.screens.home

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

def get_current_version():
    return "0.1.0-ota_update.0+1"

def get_latest_version():
    latest_version = "0.2.0-ota_update.0+1"
    files = {
        'micropython.bin': {'url': 'http://url/micro', 'size': 1234},
        'application.bin': {'url': 'http://url/app', 'size': 1234}
        }
    return latest_version, files

class OtaUpdateScreen:
    def __init__(self):
        self._screen = lv.obj()
        self._construct()

    def load(self):
        lv.screen_load(self._screen)

    def _check_update(self):
        print("check update")
        latest_version, latest_files = get_latest_version()

        screen = self._screen
        # latest version
        v_lbl = lv.label(screen)
        v_lbl.set_text("Latest version:")
        v_lbl.align(lv.ALIGN.TOP_MID, -100, 60)
        v_lbl2 = lv.label(screen)
        v_lbl2.set_text(latest_version)
        v_lbl2.align(lv.ALIGN.TOP_MID, 100, 60)

        # update button
        sv = ButtonLabel(screen, lv.SYMBOL.DOWNLOAD + " update", self._update)
        sv.btn.align_to(v_lbl, lv.ALIGN.OUT_BOTTOM_MID, 160, 0)
        # cancel button
        cn = ButtonLabel(screen, lv.SYMBOL.CLOSE + " cancel", self._cancel)
        cn.btn.align_to(v_lbl, lv.ALIGN.OUT_BOTTOM_MID, 40, 0)

    def _cancel(self):
        print("cancel")
        home_screen = fri3d.screens.home.HomeScreen()
        home_screen.load()

    def _update(self):
        print("ota_update")
        home_screen = fri3d.screens.home.HomeScreen()
        home_screen.load()
        
    def _construct(self):
        screen = self._screen

        # title
        title = lv.label(screen)
        title.set_text("Ota Update")
        title.align(lv.ALIGN.TOP_MID, 0, 0)

        # current version
        v_lbl = lv.label(screen)
        v_lbl.set_text("Current version:")
        v_lbl.align_to(title, lv.ALIGN.OUT_BOTTOM_MID, -100, 0)
        v_lbl2 = lv.label(screen)
        v_lbl2.set_text(get_current_version())
        v_lbl2.align_to(title, lv.ALIGN.OUT_BOTTOM_MID, 100, 0)

        # check button
        sv = ButtonLabel(screen, lv.SYMBOL.REFRESH + " check for update", self._check_update)
        sv.btn.align_to(v_lbl, lv.ALIGN.OUT_BOTTOM_MID, 100, 0)

