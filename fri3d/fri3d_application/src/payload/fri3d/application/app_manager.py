import json
import os
import sys

from .app_info import AppInfo
from .log import logger
from .theme_manager import ThemeManager
from .window_manager import WindowManager


class AppManager:
    def __init__(self, theme_manager: ThemeManager, window_manager: WindowManager):
        self.apps: {str, AppInfo} = {}
        self._app_instances = {}

        self._paths = [
            '/remote/fri3d/apps',
            '/remote/user',
            '/fri3d/apps',
            '/user',
            '/sdcard/user',
        ]

        # Make sure apps in sdcard get picked up
        sys.path.insert(0, '/sdcard')

        from .managers import Managers
        self._managers = Managers(
            app_manager=self,
            theme_manager=theme_manager,
            window_manager=window_manager,
        )

    def _scan_path(self, path: str):
        """
        Scan the given path for packages that contain an app.json and add them to the library
        :param path: path to scan
        """
        logger.info(f"Scanning `{path}`.")

        if not os.path.isdir(path):
            logger.info(f"Path `{path}` does not exist.")
            return

        for item in os.listdir(path):
            package_path = os.path.join(path, item)
            json_path = os.path.join(package_path, 'app.json')

            # The directory should contain an app.json file
            if os.path.isfile(json_path):
                try:
                    with open(json_path, 'r') as f:
                        app_config = json.load(f)
                        package = package_path \
                            .lstrip('/') \
                            .lstrip('remote/') \
                            .lstrip('sdcard/') \
                            .replace('/', '.')

                        orig_app = self.apps.get(package, None)

                        if orig_app:
                            logger.info(f"Duplicate package `{package}` found, this will be ignored.")
                        else:
                            app = AppInfo(
                                id=package,
                                configuration=app_config,
                            )

                            self.apps[package] = app
                            logger.info(f"Found app `{app.name}` in package `{package}`.")

                except Exception as e:
                    logger.info(f"Could not parse `{json_path}`: {e}")
                    continue

    def _load_app(self, app_id: str):
        app = self._app_instances.get(app_id, None)

        if not app:
            logger.info(f"Loading {app_id}")
            app_info = self.apps[app_id]

            # Try to load the app
            module = __import__(app_id)
            for i in app_id.split('.')[1:]:
                module = getattr(module, i)
            cls = getattr(module, app_info.cls)

            # Instantiate app
            app = cls(app_info, self._managers)
            self._app_instances[app_id] = app

        return app

    def _unload_app(self, app_id: str):
        if app_id in self._app_instances:
            self._app_instances.pop(app_id)

    async def start_app(self, app_id: str):
        if app_id not in self.apps:
            logger.error(f"App `{app_id}` not found")

        app = self._load_app(app_id)

        await app.start()

    async def stop_app(self, app_id: str):
        if app_id not in self.apps:
            logger.error(f"App `{app_id}` not found")

        app = self._app_instances.get(app_id, None)

        if app:
            await app.stop()

    async def run_app(self, app_id: str):
        await self.start_app(app_id)
        await self.stop_app(app_id)

    def scan(self):
        """
        Scan all known locations for new apps.

        Note that this function will not replace existing apps with updated versions should you change the code through
        REPL. Once code is loaded it does not get replaced, you should reset the device.
        """

        for item in self._paths:
            self._scan_path(item)

    def init(self):
        self.scan()
