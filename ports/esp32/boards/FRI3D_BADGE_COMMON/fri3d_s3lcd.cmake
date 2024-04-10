# We (ab)use MicroPython's submodule system to include our dependencies in the sync
list(APPEND GIT_SUBMODULES
    fri3d/s3lcd
)

# Inject the driver as a user module
list(APPEND USER_C_MODULES
    ../../../fri3d/s3lcd/src/micropython.cmake
)
