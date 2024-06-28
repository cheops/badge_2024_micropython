import network
import gc
import time
import logging

logger = logging.Logger('wifi_manager')

def _get_user_aps():
    return []

def _get_default_aps():
    return [{'ssid': 'fri3d-badge', 'key': 'fri3d2024'}]

def _get_aps():
    return _get_user_aps() + _get_default_aps()

class WifiManagerException(Exception):
    pass

class WifiManagerFailedConnectionException(WifiManagerException):
    pass

class WifiManager:
    """Manages the wifi connection
    call .do_connect() when you need wifi access
    call .do_disconnect() when you are done with the wifi access

    # call .ado_connect() when you need wifi access in async code
    # call .ado_disconnect() when you are done with the wifi access in async code

    you can also use WifiManager as a ContextManager, no need to call .do_connect() or .do_disconnect()
    ```
    with WifiManager() as wm:
        <your code here, using wifi>
    ```
    # you can also use WifiManager as an async ContextManager, no need to call .ado_connect() or .ado_disconnect()
    # ```
    # async with WifiManager() as wm:
    #     <your async code here, using wifi>
    # ```
    """
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self, timeout=6):
        network.country('BE')
        self._wlan = network.WLAN(network.STA_IF)
        self._aps = _get_aps()
        self._wrc = 0
        self._timeout = timeout

    def __enter__(self):
        self.do_connect()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            logger.warning(f"{exc_type=} {exc_value=} {exc_tb=}")
        self.do_disconnect()

    # async def __aenter__(self):
    #     pass

    # async def __aexit__(self, exc_t, exc_v, exc_tb):
    #     pass

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
        logger.debug(f"connecting to network '{ssid}'")
        try:
            self._wlan.connect(ssid, key)
        except Exception as e:
            logger.debug("Ignoring Exception '%s', let's first wait the timeout, it might recover", e.value)
            pass
        
        timeout = self._timeout * 1000
        while self._wlan.status() != network.STAT_GOT_IP:
            time.sleep_ms(50)
            timeout -= 50
            if timeout < 0:
                logger.error("timeout (%d sec) failed to connect to '%s'", self._timeout, ssid)
                break
            pass

        if self._wlan.status() == network.STAT_GOT_IP:
            logger.debug('network config: %s', self._wlan.ifconfig())
            self._wrc += 1   
            self._last_known_ap(ssid, key)
            return

        elif self._wlan.status() == network.STAT_NO_AP_FOUND:
            logger.error("ssid: %s: no AP found", ssid)
        elif self._wlan.status() == network.STAT_WRONG_PASSWORD:
            logger.error("ssid: %s: wrong password", ssid)
        elif self._wlan.status() == network.STAT_BEACON_TIMEOUT:
            logger.error("ssid: %s: beacon timeout", ssid)
        elif self._wlan.status() == network.STAT_ASSOC_FAIL:
            logger.error("ssid: %s: association failed", ssid)
        elif self._wlan.status() == network.STAT_HANDSHAKE_TIMEOUT:
            logger.error("ssid: %s: handshake timeout", ssid)
        elif self._wlan.status() == network.STAT_IDLE:
            logger.error("network is IDLE, it should be connected")
        elif self._wlan.status() == network.STAT_CONNECTING:
            logger.error("network is CONNECTING, it should be connected")
        else:
            logger.error("unkown wifi status: %d", self._wlan.status())
        
        self._wlan.disconnect()
        time.sleep_ms(50)

    def do_connect(self):
        "tries to connect to all known aps in order: nvs, fri3d-default"
        self._wlan.active(True)
        if not self._wlan.isconnected():
            for ap in _get_aps():
                self._connect(ap['ssid'], ap['key'])
                if self._wlan.isconnected():
                    break
            
            if not self._wlan.isconnected():
                logger.error("failed to connect to known access points, disabling Wifi")
                self._wlan.disconnect()
                self._wlan.active(False)
                time.sleep_ms(50)
                gc.collect()
                raise WifiManagerFailedConnectionException("failed to connect to known access points, disabled Wifi")
            

    def do_disconnect(self):
        self._wrc -= 1
        if self._wrc == 0:
            logger.debug("disconnecting from network")
            self._wlan.disconnect()
            self._wlan.active(False)
            time.sleep_ms(50)
            gc.collect()
            logger.debug("disabled Wifi")
