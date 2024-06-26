from .app_manager import AppManager
from .theme_manager import ThemeManager
from .window_manager import WindowManager


class Managers:
    """Convenience class to easily pass managers to apps"""
    def __init__(
            self,
            app_manager: AppManager,
            theme_manager: ThemeManager,
            window_manager: WindowManager,
    ):
        self.app_manager = app_manager
        self.theme_manager = theme_manager
        self.window_manager = window_manager
