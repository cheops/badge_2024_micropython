import asyncio
import lvgl as lv

from fri3d.application import App
from fri3d.badge.leds import leds


class Splash(App):
    def __init__(
            self,
            info: AppInfo,
            managers: Managers,
    ):
        super().__init__(info, managers)

    async def flash_leds(self):
        self.logger.debug("Flashing LEDs")

        # cycle
        for i in range(4 * leds.n):
            for j in range(leds.n):
                leds[j] = (0, 0, 0)
            leds[i % leds.n] = (255, 255, 255)
            leds.write()
            await asyncio.sleep_ms(25)

        # bounce
        for i in range(4 * leds.n):
            for j in range(leds.n):
                leds[j] = (0, 0, 128)
            if (i // leds.n) % 2 == 0:
                leds[i % leds.n] = (0, 0, 0)
            else:
                leds[leds.n - 1 - (i % leds.n)] = (0, 0, 0)
            leds.write()
            await asyncio.sleep_ms(60)

        # fade in/out
        for i in range(0, 4 * 256, 8):
            for j in range(leds.n):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                leds[j] = (val, 0, 0)
            leds.write()
            await asyncio.sleep(0)

        # clear
        for i in range(leds.n):
            leds[i] = (0, 0, 0)
        leds.write()

    @staticmethod
    async def splash_screen():
        screen = lv.screen_active()

        label = lv.label(screen)
        label.set_text("SPLASH SCREEN")
        label.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN)
        label.align(lv.ALIGN.CENTER, 0, 0)

        a = lv.anim_t()
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

        await asyncio.sleep(3)

        # Clean up after ourselves
        lv.anim_delete(label, None)
        label.delete()

    async def start(self):
        self.logger.info("Performing splash")
        flash = asyncio.create_task(self.flash_leds())
        screen = asyncio.create_task(self.splash_screen())

        await asyncio.gather(*[flash, screen])
