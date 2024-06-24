import logging
import os

from p0tat0.sys import dev_mode

# If you connect GPIO2 of the SAO connector to the GND pin, the dev mode gets activated, and we automatically drop to
# REPL
#
# This is easier than the Ctrl+A, Ctrl+D, Ctrl+B procedure and allows for faster development cycles: you can mount your
# local development scripts using `mpremote mount` and # perform any actions you like. On first execution of
# `mpremote mount`, it will start in RAW REPL mode meaning this `main.py` does not get imported. On subsequent
# soft-reboots (press Ctrl+D) it does automatically get run because the firmware stays in FRIENDLY REPL mode. If we
# would not drop to REPL here, the remount after soft-reboot would not work
#
# Note that if you do not connect the pin and use `mpremote mount` you can still use the classic procedure and this file
# is basically a no-op.

if dev_mode.is_active():
    logging.warning("Dev mode is active, dropping to REPL")

else:
    if 'main.py' in os.listdir():
        import main
