#define SPNG_USE_MINIZ
// #include "spng.h"
#include "../../libspng/spng/spng.c"

#include "py/runtime.h"

STATIC const mp_rom_map_elem_t spng_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_spng) },
};
STATIC MP_DEFINE_CONST_DICT(spng_module_globals, spng_module_globals_table);

const mp_obj_module_t spng_user_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&spng_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_spng, spng_user_module, 1);
