set(IDF_TARGET esp32s3)

set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.base
    boards/sdkconfig.usb
    boards/sdkconfig.ble
    boards/sdkconfig.240mhz
    boards/sdkconfig.spiram_sx
    boards/sdkconfig.spiram_oct
    boards/FRI3D_BADGE_COMMON/sdkconfig.partition
    boards/FRI3D_BADGE_2024/sdkconfig.board
)

set(MICROPY_FROZEN_MANIFEST ${MICROPY_BOARD_DIR}/manifest.py)

include (${MICROPY_BOARD_DIR}/../FRI3D_BADGE_COMMON/fri3d_s3lcd.cmake)
