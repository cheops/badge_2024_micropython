import asyncio
import lvgl_esp32
import lvgl as lv

from fri3d.badge.display import display
from fri3d.indev.indev import Indev

from .app_manager import AppManager
from .log import logger
from .theme_manager import ThemeManager
from .window_manager import WindowManager


class Application:
    def __init__(self, default_app: str = 'fri3d.apps.launcher'):
        logger.info("Configuring application")
        self.running = False

        self._wrapper = lvgl_esp32.Wrapper(display)
        self._wrapper.init()

        self._indev = Indev()

        self._theme_manager = ThemeManager()
        self._window_manager = WindowManager()
        self._app_manager = AppManager(self._theme_manager, self._window_manager)

        self._default_app = default_app

    async def lvgl_tick(self):
        while self.running:
            # sleep_ms can't handle too big values, so we limit it to 40 ms, which equals 25 fps
            sleep_time = min(lv.timer_handler(), 40)
            await asyncio.sleep_ms(sleep_time)

    async def _main(self):
        self._theme_manager.init()
        self._window_manager.init()
        self._app_manager.init()

        tick = asyncio.create_task(self.lvgl_tick())

        await self._app_manager.run_app(self._default_app)

        self.running = False

        await tick

    def run(self):
        logger.info("Starting application")
        self.running = True

        asyncio.run(self._main())
