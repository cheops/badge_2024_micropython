import network

def get_ssid_key_from_secrets():
    try:
        from .secrets import ssid
        from .secrets import key
        return ssid, key
    except:
        return None, None

def get_ssid_key_from_nvs():
    return None, None

def get_ssid_key():
    ssid, key = get_ssid_key_from_secrets()
    if ssid is None and key is None:
        ssid, key = get_ssid_key_from_nvs()
        if ssid is None and key is None:
            ssid, key = ('fri3d-badge', 'fri3d2024')
    return ssid, key


class WifiManager:
    def __init__(self):
        self._wlan = network.WLAN(network.STA_IF)
        self._ssid, self._key = get_ssid_key()
        self._wrc = 0

    def do_connect(self):
        self._wlan.active(True)
        if not self._wlan.isconnected():
            print('connecting to network...')
            self._wlan.connect(self._ssid, self._key)
            while not self._wlan.isconnected():
                pass
        print('network config:', self._wlan.ifconfig())
        self._wrc += 1

    def do_disconnect(self):
        self._wrc -= 1
        if self._wrc == 0:
            print("disconnecting from network")
            self._wlan.disconnect()
            self._wlan.active(False)
