import lvgl as lv


class ThemeManager:
    def __init__(self):
        pass

    def init(self):
        # Very basic theme for now
        display = lv.display_get_default()

        theme = lv.theme_default_init(
            display,
            lv.palette_main(lv.PALETTE.GREEN),
            lv.palette_main(lv.PALETTE.GREY),
            True,
            lv.font_montserrat_16,
        )

        display.set_theme(theme)
