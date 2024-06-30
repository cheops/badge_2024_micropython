import network
import gc
import time
import logging
import asyncio

logger = logging.Logger('fri3d.application.wifi_manager')

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
    
    Keeps a reference counter for the amount of times connected + disconnected.
    When reaching 0 shut's down the wifi.
    
    ## Sync code
    - call `.do_connect()` when you need wifi access
    - call `.do_disconnect()` when you are done with the wifi access

    you can also use WifiManager as a ContextManager, no need to call .do_connect() or .do_disconnect()
    ```
    with WifiManager():
        <your code here, using wifi>
    ```

    ## Async code
    - call `await .ado_connect()` when you need wifi access in async code
    - call `await .ado_disconnect()` when you are done with the wifi access in async code

    you can also use WifiManager as an async ContextManager, no need to call await .ado_connect() or await .ado_disconnect()
    ```
    async with WifiManager():
        <your async code here, using wifi>
    ```
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

    async def __aenter__(self):
        await self.ado_connect()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            logger.warning(f"{exc_type=} {exc_value=} {exc_tb=}")
        await self.ado_disconnect()

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
        logger.debug("connecting to network '%s'", ssid)
        try:
            self._wlan.connect(ssid, key)
        except Exception as e:
            logger.debug("Ignoring Exception '%s', let's first wait the timeout, it might recover", e.value)
            pass
        
        start_ticks = time.ticks_ms()
        while self._wlan.status() != network.STAT_GOT_IP:
            time.sleep_ms(50)
            if time.ticks_diff(time.ticks_ms(), start_ticks) > self._timeout * 1000:
                logger.error("timeout (%d sec) failed to connect to '%s'", self._timeout, ssid)
                break
            pass

        if self._wlan.status() == network.STAT_GOT_IP:
            logger.debug('network config: %s', self._wlan.ifconfig())
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

    def _disable_wifi(self):
        self._wlan.disconnect()
        self._wlan.active(False)
        time.sleep_ms(50)
        gc.collect()

    def do_connect(self):
        "tries to connect to all known aps in order: nvs, fri3d-default"
        if not self._wlan.active():
            self._wlan.active(True)
        if not self._wlan.isconnected():
            for ap in _get_aps():
                self._connect(ap['ssid'], ap['key'])
                if self._wlan.isconnected():
                    break
            
            if not self._wlan.isconnected():
                logger.error("failed to connect to known access points, disabling Wifi")
                self._disable_wifi()
                raise WifiManagerFailedConnectionException("failed to connect to known access points, disabled Wifi")
        self._wrc += 1

    def do_disconnect(self):
        self._wrc -= 1
        if self._wrc == 0:
            logger.debug("disconnecting from network")
            self._disable_wifi()
            logger.debug("disabled Wifi")

    async def _aconnect(self, ssid, key):
        logger.debug("connecting to network '%s'", ssid)
        try:
            self._wlan.connect(ssid, key)
        except Exception as e:
            logger.debug("Ignoring Exception '%s', let's first wait the timeout, it might recover", e.value)
            pass
        
        start_ticks = time.ticks_ms()
        while self._wlan.status() != network.STAT_GOT_IP:
            await asyncio.sleep_ms(50)
            if time.ticks_diff(time.ticks_ms(), start_ticks) > self._timeout * 1000:
                logger.error("timeout (%d sec) failed to connect to '%s'", self._timeout, ssid)
                break
            pass

        if self._wlan.status() == network.STAT_GOT_IP:
            logger.debug('network config: %s', self._wlan.ifconfig())
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
        await asyncio.sleep_ms(50)

    async def _adisable_wifi(self):
        self._wlan.disconnect()
        self._wlan.active(False)
        await asyncio.sleep_ms(50)
        gc.collect()

    async def ado_connect(self):
        "tries to connect to all known aps in order: nvs, fri3d-default"
        if not self._wlan.active():
            self._wlan.active(True)
        if not self._wlan.isconnected():
            for ap in _get_aps():
                await self._aconnect(ap['ssid'], ap['key'])
                if self._wlan.isconnected():
                    break
            
            if not self._wlan.isconnected():
                logger.error("failed to connect to known access points, disabling Wifi")
                await self._adisable_wifi()
                raise WifiManagerFailedConnectionException("failed to connect to known access points, disabled Wifi")
        self._wrc += 1

    async def ado_disconnect(self):
        self._wrc -= 1
        if self._wrc == 0:
            logger.debug("disconnecting from network")
            await self._adisable_wifi()
            logger.debug("disabled Wifi")
