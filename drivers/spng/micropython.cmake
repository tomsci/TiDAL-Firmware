# Create an INTERFACE library for our C module.
add_library(usermod_spng INTERFACE)


# Add our source files to the lib
target_sources(usermod_spng INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/spng_wrapper.c
    ${CMAKE_CURRENT_LIST_DIR}/../../libspng/spng.c

)

target_include_directories(usermod_spng INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/../../libspng
)

target_compile_definitions(usermod_spng INTERFACE
    SPNG_USE_MINIZ=1
)


# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE usermod_spng)

add_subdirectory("../../miniz")
