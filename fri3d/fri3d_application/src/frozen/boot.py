# At boot time, MicroPython will start any `boot.py` it finds automatically, but because we freeze this file it does not
# show up in the filesystem and gets priority over the automatically generated `boot.py` that MicroPython puts in /.
#
# This means that we can do pretty much any initialization we want to do here before we hand control over to the part
# of badge code the end-user can hack.
import logging
import machine
import os

from p0tat0.sys import flash, dev_mode


def check_dev_mode():
    from fri3d.badge.hardware import hardware_sao

    repl_pin = machine.Pin(hardware_sao.pinout.gpio2, machine.Pin.IN, machine.Pin.PULL_UP)

    if repl_pin.value() == 0:
        logging.info("Detected REPL pin active, activating dev mode.")
        dev_mode.activate()


# We temporarily set logging to INFO because these messages can not be caught by setting it in main.py
logging.basicConfig(level=logging.INFO)

logging.info("Fri3d Camp Badge booting")
# Make sure the flash is in a proper state
flash.init_internal_flash()

# Check if we need to activate dev mode
check_dev_mode()

# Restore default log level
logging.basicConfig(level=logging.WARNING, force=True)

# Finally, we import the actual `boot.py` on the VFS if it exists, which the user can freely edit
if 'boot.py' in os.listdir():
    import boot
