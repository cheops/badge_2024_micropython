from fri3d.application import App, AppInfo, Managers


class ExampleApp(App):
    def __init__(
            self,
            info: AppInfo,
            managers: Managers,
    ):
        # Do not forget to pass the variables to the base class
        super().__init__(info, managers)

        # The base class provides a logger attribute which is a pre-configured logging.Logger instance
        self.logger.info("Configuring Example App")

        self._answer = self.config.get('answer', None)

    async def start(self):
        self.logger.info(f"The Answer to the Ultimate Question of Life, the Universe, and Everything is {self._answer}")

    # async def stop(self):
    #     self.logger.info("Stopping Example App")
