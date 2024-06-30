class AppInfo:
    def __init__(
            self,
            id: str,
            configuration: dict,
    ):
        self.id = id

        self.name = configuration.get('name', None)
        if not self.name:
            raise AttributeError("Required key `name` not found")

        self.cls = configuration.get('cls', None)
        if not self.cls:
            raise AttributeError("Required key `cls` not found")

        # Whether the app should be hidden from the launcher or not
        self.hidden = configuration.get('hidden', False)

        # App specific configuration
        self.config = configuration.get('config', {})
