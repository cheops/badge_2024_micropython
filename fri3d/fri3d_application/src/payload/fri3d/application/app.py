import logging

from .app_info import AppInfo
from .managers import Managers


class App:
    def __init__(
            self,
            info: AppInfo,
            managers: Managers
    ):
        self._info = info
        self._managers = managers

        # Logger
        self.logger = logging.Logger(self.id)

    async def start(self):
        """
        An app should at least implement this function. It can start new async tasks but if it does it should keep track
        of them and await them in the stop function.
        """
        raise NotImplementedError("Start function not yet implemented")

    async def stop(self):
        """
        This function does not need to be implemented if there are no resources (like async tasks, ...) to be released
        """
        self.logger.info("No stop function implemented, skipping")

    # Convenience properties
    @property
    def id(self):
        return self._info.id

    @property
    def name(self):
        return self._info.name

    @property
    def hidden(self):
        return self._info.hidden

    @property
    def config(self):
        return self._info.config

    @property
    def app_manager(self):
        return self._managers.app_manager

    @property
    def theme_manager(self):
        return self._managers.theme_manager

    @property
    def window_manager(self):
        return self._managers.window_manager
