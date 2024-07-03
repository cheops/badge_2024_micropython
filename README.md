# Fri3d Badge MicroPython

This repository builds the default firmware for the badges handed out at Fri3d camp. The firmware is a fork of 
MicroPython and adds its own libraries.

You can find the original README.md of the MicroPython project 
[here](https://github.com/micropython/micropython/blob/v1.22.2/README.md).

## Repository structure

The following branches are available in this repository:

* develop: bleeding edge development, do not use unless you know what you are doing
* stable: safe for general use

The firmware is built on top of and tested with specific upstream versions:

* MicroPython: v1.23
* ESP-IDF: v5.2.2

## Building

Building should work by following [the manual](https://docs.micropython.org/en/latest/develop/gettingstarted.html)
of MicroPython.

As a quick reference, here is a short summary:

* Install build dependencies
* Install the version of ESP-IDF above and source the `export.sh` script
* Check out this repository locally and `cd` into it
* `make -C mpy-cross`
* `cd ports/esp32`
* `export PORT=<device>` but replace `<device>` with the actual device
  * Default is `/dev/ttyUSB0` which works for the 2022 badge in which case you can skip this step
  * The 2024 badge uses another driver and will be `/dev/ttyACM0`
  * If you have multiple badges attached the number will be increase, ie `/dev/ttyUSB1`, `/dev/ttyACM6`, ...
* `export BOARD=FRI3D_BADGE_2024`
  * Use `FRI3D_BADGE_2024` for the 2024 Badge
  * Use `FRI3D_BADGE_2022` for the 2022 Badge
* `make submodules`
* `make`
* `make erase` if there was no MicroPython on the badge previously
* `make deploy` to flash the badge

Congratulations, you should now be able to connect to the Python prompt

## Connecting
There are multiple options:
* ESP-IDF monitor  
  `BAUD=115200 make monitor` to connect to the serial interface (which adds automatic backtrace decoding)

* screen  
  Replace `/dev/ttyACM0` with the correct device

```
screen /dev/ttyACM0 115200
```
* picocom
```
picocom -b 115200 /dev/ttyACM0
```

## backtrace decoding
* terminal with buildin decoding: `BAUD=115200 make monitor`
* `function esp32-backtrace() { xtensa-esp32-elf-addr2line -pfiaC -e build-${BOARD}/micropython.elf "$@"; }`  
  creates a command function for backtrace decoding  
  can be used like this `esp32-backtrace <paste the backtrace here>`  
  you can put it in your `~/.bashrc` file

