import asyncio
import lvgl_esp32
import lvgl as lv

from fri3d.badge.display import display
from fri3d.indev.indev import Indev
from fri3d.splash import Splash

from .log import logger


class Launcher:
    def __init__(self):
        logger.info("Configuring launcher")
        self.running = False

        self._wrapper = lvgl_esp32.Wrapper(display)
        self._wrapper.init()

        self.indev = Indev()

    async def lvgl_tick(self):
        while self.running:
            # sleep_ms can't handle too big values, so we limit it to 40 ms, which equals 25 fps
            sleep_time = min(lv.timer_handler(), 40)
            await asyncio.sleep_ms(sleep_time)

    async def main(self):
        screen = lv.screen_active()
        screen.set_style_bg_color(lv.palette_darken(lv.PALETTE.GREY, 4), lv.PART.MAIN)

        tick = asyncio.create_task(self.lvgl_tick())

        splash = Splash()
        await splash.run()

        while self.running:
            await asyncio.sleep(5)

        await tick

    def run(self):
        logger.info("Starting launcher")
        self.running = True

        asyncio.run(self.main())
