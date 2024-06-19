find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(FRI3D_APPLICATION_C     ${CMAKE_BINARY_DIR}/fri3d_application.c)
set(FRI3D_PACKAGE_PY        ${CMAKE_CURRENT_LIST_DIR}/src/package.py)
set(FRI3D_PAYLOAD           ${CMAKE_CURRENT_LIST_DIR}/src/payload)

# If any of the payload files changes we need to repackage the payload
file(GLOB_RECURSE FRI3D_PAYLOAD_FILES "${FRI3D_PAYLOAD}/*.py")

add_custom_command(
    OUTPUT
        ${FRI3D_APPLICATION_C}
    COMMAND
        ${Python3_EXECUTABLE}
            ${FRI3D_PACKAGE_PY}
            ${FRI3D_PAYLOAD}
            ${FRI3D_APPLICATION_C}
    DEPENDS
        ${FRI3D_PACKAGE_PY}
        ${FRI3D_PAYLOAD_FILES}
    COMMAND_EXPAND_LISTS
)

# Temporarily create an empty file to keep IDF happy
file(WRITE ${FRI3D_APPLICATION_C} "")

add_library(usermod_fri3d_application INTERFACE)

target_sources(usermod_fri3d_application INTERFACE
        ${FRI3D_APPLICATION_C}
        ${CMAKE_CURRENT_LIST_DIR}/src/c/module.c
)

target_compile_definitions(usermod_fri3d_application INTERFACE
        ${MICROPY_BOARD}
)
target_include_directories(usermod_fri3d_application INTERFACE
        ${CMAKE_CURRENT_LIST_DIR}/src/c/include
)

target_link_libraries(usermod INTERFACE usermod_fri3d_application)
