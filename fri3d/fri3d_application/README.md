This module contains the actual application that runs on the Fri3d badges.
* At compile time the CMake code creates a .tar.gz of the `src/payload` directory
* The binary blob gets embedded as C code into the firmware
* The code in `src/frozen` (amongst other things) extracts the binary blob when necessary on the device at boot time
