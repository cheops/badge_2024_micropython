from fri3d.application import App, AppInfo, Managers


class Launcher(App):
    def __init__(
            self,
            info: AppInfo,
            managers: Managers,
    ):
        super().__init__(info, managers)
        self.logger.info("Configuring launcher")

        self._splash = self.config.get('splash', None)

    async def start(self):
        self.logger.info("Starting launcher")

        if self._splash:
            await self.app_manager.run_app(self._splash)
        await self.app_manager.run_app('fri3d.apps.ota_update')

    async def stop(self):
        self.logger.info("Stopping launcher")
