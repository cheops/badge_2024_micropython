import deflate
import esp32
import io
import inisetup
import logging
import os
import tarfile

from flashbdev import bdev

from _p0tat0 import application_data, application_digest


_logger = logging.Logger('p0tat0.sys.flash')
_nvs = esp32.NVS('p0tat0.sys')
_DIGEST_KEY = 'digest'


def _clear_bootsec():
    buf = bytearray([0xFF] * bdev.ioctl(5, 0))  # 5 is SEC_SIZE
    bdev.writeblocks(0, buf)


def wipe_internal_flash():
    # Mark the digest as invalid
    try:
        _nvs.erase_key(_DIGEST_KEY)
    except OSError:
        pass

    # Unmount the internal flash
    os.umount('/')

    # We need to clear the boot sector or inisetup will complain about a corrupt FS
    _clear_bootsec()

    # Format the internal flash
    inisetup.setup()


def init_internal_flash():
    digest = application_digest()
    nvs_digest = bytearray(16)
    try:
        _nvs.get_blob(_DIGEST_KEY, nvs_digest)
    except OSError:
        pass

    if digest != nvs_digest:
        _logger.warning("Application digest does not match firmware, wiping internal flash")
        wipe_internal_flash()

    old_path = os.getcwd()

    # Change to the root directory
    os.chdir('/')
    entries = os.listdir()

    missing = []

    for item in ['main.py', 'fri3d', 'user', 'examples']:
        if item not in entries:
            _logger.info(f"{item} not found, restoring")
            missing.append(item)

    if len(missing) > 0:
        compressed_data = application_data()

        _logger.info("Opening archive")
        with deflate.DeflateIO(io.BytesIO(compressed_data), deflate.GZIP) as tar_data:
            tar = tarfile.TarFile(fileobj=tar_data)

            _logger.info("Extracting files")
            for tar_item in tar:
                start = tar_item.name.split('/',1)[0]

                if start in missing:
                    if tar_item.type == tarfile.DIRTYPE:
                        _logger.debug(f"Creating `{tar_item.name}`")
                        os.mkdir(tar_item.name.rstrip('/'))
                    else:
                        _logger.debug(f"Extracting `{tar_item.name}`")
                        tar_file = tar.extractfile(tar_item)
                        with open(tar_item.name, 'wb') as f:
                            f.write(tar_file.read())

        _nvs.set_blob(_DIGEST_KEY, digest)
        _nvs.commit()
        _logger.info("Done")

    # Go back to where we were
    os.chdir(old_path)
