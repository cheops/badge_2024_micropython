# esp32_ota module for MicroPython on ESP32
# MIT license; Copyright (c) 2023 Glenn Moloney @glenn20

# Inspired by OTA class by Thorsten von Eicken (@tve):
#   https://github.com/tve/mqboard/blob/master/mqrepl/mqrepl.py

import gc
import io
import aiohttp

from esp32 import Partition

from .blockdev_writer import BlockDevWriter
from .status import ota_reboot

# OTA manages a MicroPython firmware update over-the-air. It checks that there
# are at least two "ota" "app" partitions in the partition table and writes new
# firmware into the partition that is not currently running. When the update is
# complete, it sets the new partition as the next one to boot. Set reboot=True
# to force a reset/restart, or call machine.reset() explicitly. Remember to call
# ota.rollback.cancel() after a successful reboot to the new image.
class OTA:
    def __init__(self, verify=True, verbose=True, reboot=False, sha="", length=0):
        self.reboot = reboot
        self.verbose = verbose
        # Get the next free OTA partition
        # Raise OSError(ENOENT) if no OTA partition available
        self.part = Partition(Partition.RUNNING).get_next_update()
        if verbose:
            name: str = self.part.info()[4]
            print(f"Writing new micropython image to OTA partition '{name}'...")
        self.writer = BlockDevWriter(self.part, verify, verbose)
        if sha or length:
            self.writer.set_sha_length(sha, length)

    # Append the data to the OTA partition
    def write(self, data: bytearray | bytes | memoryview) -> int:
        return self.writer.write(data)

    # Flush any buffered data to the ota partition and set it as the boot
    # partition. If verify is True, will read back the written firmware data to
    # check the sha256 of the written data. If reboot is True, will reboot the
    # device after 10 seconds.
    def close(self) -> None:
        if self.writer is None:
            return
        self.writer.close()
        # Set as boot partition for next reboot
        name: str = self.part.info()[4]
        print(f"OTA Partition '{name}' updated successfully.")
        self.part.set_boot()  # Raise OSError(-5379) if image on part is not valid
        bootname = Partition(Partition.BOOT).info()[4]
        if name != bootname:
            print(f"Warning: failed to set {name} as the next boot partition.")
        print(f"Micropython will boot from '{bootname}' partition on next boot.")
        print("Remember to call ota.rollback.cancel() after successful reboot.")
        if self.reboot:
            ota_reboot()

    def __enter__(self):
        return self

    def __exit__(self, e_t, e_v, e_tr):
        if e_t is None:  # If exception is thrown, don't flush data or set bootable
            self.close()

    # Load a firmware file from the provided io stream
    # - f: an io stream (supporting the f.readinto() method)
    # - sha: (optional) the sha256sum of the firmware file
    # - length: (optional) the length (in bytes) of the firmware file
    async def afrom_stream(self, f: io.BufferedReader, sha: str = "", length: int = 0) -> int:
        if sha or length:
            self.writer.set_sha_length(sha, length)
        gc.collect()
        return await self.writer.awrite_from_stream(f)

    # Write new firmware to the OTA partition from the given url
    # - url: a filename or a http[s] url for the micropython.bin firmware.
    # - sha: the sha256sum of the firmware file
    # - length: the length (in bytes) of the firmware file
    async def afrom_firmware_url(self, url: str, sha: str = "", length: int = 0, headers={}) -> int:
        if self.verbose:
            print(f"Opening firmware url {url}")

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as r:
                code: int = r.status
                content = r.content
                if code != 200:
                    r_text = await r.text()
                    print(r_text)
                    await r.wait_closed()
                    raise ValueError(f"HTTP Error: {code}")
                
                tot_bytes = await self.afrom_stream(content, sha, length)
        
        return tot_bytes


# Convenience functions which use the OTA class to perform OTA updates.
async def afrom_url(
    url: str, sha="", length=0, verify=True, verbose=True, reboot=True, headers={}
) -> None:
    with OTA(verify, verbose, reboot) as ota_update:
        await ota_update.afrom_firmware_url(url, sha, length, headers)

