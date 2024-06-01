from .pinout import hardware_pinout


class HardwareBatteryMonitor:
    def __init__(self):
        self.pinout = hardware_pinout.pinout_battery_monitor


hardware_battery_monitor = HardwareBatteryMonitor()