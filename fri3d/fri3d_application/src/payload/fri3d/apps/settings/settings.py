from fri3d.application import App, AppInfo, Managers


class Settings(App):
    def __init__(
            self,
            info: AppInfo,
            managers: Managers,
    ):
        super().__init__(info, managers)

    async def start(self):
        self.logger.info(f"Launching {self.name}")
