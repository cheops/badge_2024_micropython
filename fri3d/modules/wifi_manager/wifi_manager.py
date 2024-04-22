import network
import gc
import time

from fri3d import logging
from fri3d.settings_nvs import read_blob, toml_blob_to_dict

log = logging.Log(__name__, level=logging.DEBUG)

def _get_nvs_aps():
    "read toml settings from nvs"
    d = toml_blob_to_dict(read_blob('system', 'wifi'))
    return d['aps']

def _get_default_aps():
    return [{'ssid': 'fri3d-badge', 'key': 'fri3d2024'}]

def _get_aps():
    return _get_nvs_aps() + _get_default_aps()

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
        self._aps = _get_aps()
        self._wrc = 0

    def __enter__(self):
        self.do_connect()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            log.warning(f"{exc_type=} {exc_value=} {exc_tb=}")
        self.do_disconnect()

    def _last_known_ap(self, ssid, key):
        "put the last known ap in front, so that is tried first next time"
        for i, ap in enumerate(self._aps):
            if ap['ssid'] == ssid:
                self._aps.insert(0, self._aps.pop(i))
                break

    @property
    def wlan(self):
        return self._wlan

    def _connect(self, ssid, key):
        log.debug(f"connecting to network '{ssid}'")
        self._wlan.connect(ssid, key)
        timeout = 3000
        while self._wlan.status() == network.STAT_CONNECTING or self._wlan.status() == network.STAT_IDLE:
            time.sleep_ms(50)
            timeout -= 50
            if timeout < 0:
                log.error("timeout (3sec) failed to connect to '{ssid}'")
                break
            pass

        if self._wlan.status() == network.STAT_GOT_IP:
            log.debug(f'network config: {self._wlan.ifconfig()}')
            self._wrc += 1   
            self._last_known_ap(ssid, key)

        elif self._wlan.status() == network.STAT_NO_AP_FOUND:
            log.error(f"ssid '{ssid}' no AP found")
        elif self._wlan.status() == network.STAT_WRONG_PASSWORD:
            log.error(f"ssid '{ssid}' wrong password")
        elif self._wlan.status() == network.STAT_BEACON_TIMEOUT:
            log.error(f"ssid '{ssid}' beacon timeout")
        elif self._wlan.status() == network.STAT_ASSOC_FAIL:
            log.error(f"ssid '{ssid}' association failed")
        elif self._wlan.status() == network.STAT_HANDSHAKE_TIMEOUT:
            log.error(f"ssid '{ssid}' handshake timeout")
        elif self._wlan.status() == network.STAT_IDLE:
            log.error("network is IDLE, it should be connecting")
        else:
            log.error("unkown wifi status " + self._wlan.status())

    def do_connect(self):
        "tries to connect to all known aps in order: nvs, fri3d-default"
        self._wlan.active(True)
        if not self._wlan.isconnected():
            for ap in _get_aps():
                self._connect(ap['ssid'], ap['key'])
                if self._wlan.isconnected():
                    break
            
            if not self._wlan.isconnected():
                log.error("failed to connect to known access points")

    def do_disconnect(self):
        self._wrc -= 1
        if self._wrc == 0:
            log.debug("disconnecting from network")
            self._wlan.disconnect()
            self._wlan.active(False)

            gc.collect()
