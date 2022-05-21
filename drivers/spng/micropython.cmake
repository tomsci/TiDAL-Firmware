# Create an INTERFACE library for our C module.
add_library(usermod_spng INTERFACE)

#target_compile_definitions(usermod_spng INTERFACE SPNG_USE_MINIZ)

target_compile_options(usermod_spng INTERFACE -mlongcalls)

# Add our source files to the lib
target_sources(usermod_spng INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/spng_wrapper.c
    # Yes miniz has a cmake project. No I can't get it to work.
    ${CMAKE_CURRENT_LIST_DIR}/../../miniz/miniz.c
    ${CMAKE_CURRENT_LIST_DIR}/../../miniz/miniz_zip.c
    ${CMAKE_CURRENT_LIST_DIR}/../../miniz/miniz_tinfl.c
    ${CMAKE_CURRENT_LIST_DIR}/../../miniz/miniz_tdef.c
)

target_include_directories(usermod_spng INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/../../miniz
    ${CMAKE_CURRENT_LIST_DIR}/../../libspng/spng
)

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE usermod_spng)
