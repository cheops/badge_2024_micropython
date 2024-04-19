import network

from fri3d import logging

log = logging.Log(__name__, level=logging.DEBUG)

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
    """Manages the wifi connection
    call .do_connect() when you need wifi access
    call .do_disconnect() when you are done with the wifi access

    you can also use WifiManager as a ContextManager, no need to call .do_connect() or .do_disconnect()
    with WifiManager() as wm:
        <your code here, using wifi>
    """
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._wlan = network.WLAN(network.STA_IF)
        self._ssid, self._key = get_ssid_key()
        self._wrc = 0

    def __enter__(self):
        self.do_connect()
        return self
    
    def __exit__(self):
        self.do_disconnect()

    def do_connect(self):
        self._wlan.active(True)
        if not self._wlan.isconnected():
            log.debug('connecting to network...')
            self._wlan.connect(self._ssid, self._key)
            while not self._wlan.isconnected():
                pass
        log.debug(f'network config: {self._wlan.ifconfig()}')
        self._wrc += 1

    def do_disconnect(self):
        self._wrc -= 1
        if self._wrc == 0:
            log.debug("disconnecting from network")
            self._wlan.disconnect()
            self._wlan.active(False)
