# This file can be imported for easier development. You can trigger dev_mode by connecting GPIO2 of the SAO connector
# to the GND pin.
import sys

_dev_mode = False


def activate():
    global _dev_mode
    _dev_mode = True


def is_active():
    return _dev_mode
