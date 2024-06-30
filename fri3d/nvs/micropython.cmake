add_library(usermod_nvs INTERFACE)

target_sources(usermod_nvs INTERFACE
        ${CMAKE_CURRENT_LIST_DIR}/src/nvs.c
)

target_include_directories(usermod_nvs INTERFACE
        ${IDF_PATH}/components/nvs_flash/include/
)

target_link_libraries(usermod INTERFACE usermod_nvs)
