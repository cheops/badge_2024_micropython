#include "fri3d_application.h"

#include "py/binary.h"

#define FRI3D_BADGE_2022_TYPE 0x00
#define FRI3D_BADGE_2024_TYPE 0x01

#ifdef FRI3D_BADGE_2022
#define BADGE_TYPE FRI3D_BADGE_2022_TYPE
#endif
#ifdef FRI3D_BADGE_2024
#define BADGE_TYPE FRI3D_BADGE_2024_TYPE
#endif

static mp_obj_t p0tat0_application_data(void)
{
    return mp_obj_new_memoryview(BYTEARRAY_TYPECODE, fri3d_application_length, (void *) fri3d_application_data);
}
static MP_DEFINE_CONST_FUN_OBJ_0(p0tat0_application_data_obj, p0tat0_application_data);

static mp_obj_t p0tat0_application_digest(void)
{
    return mp_obj_new_memoryview(BYTEARRAY_TYPECODE, 16, (void *) fri3d_application_digest);
}
static MP_DEFINE_CONST_FUN_OBJ_0(p0tat0_application_digest_obj, p0tat0_application_digest);

static const mp_rom_map_elem_t p0tat0_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR__p0tat0) },
    { MP_ROM_QSTR(MP_QSTR_application_data), MP_ROM_PTR(&p0tat0_application_data_obj) },
    { MP_ROM_QSTR(MP_QSTR_application_digest), MP_ROM_PTR(&p0tat0_application_digest_obj) },
    { MP_ROM_QSTR(MP_QSTR_FRI3D_BADGE_2022), MP_ROM_INT(FRI3D_BADGE_2022_TYPE) },
    { MP_ROM_QSTR(MP_QSTR_FRI3D_BADGE_2024), MP_ROM_INT(FRI3D_BADGE_2024_TYPE) },
    { MP_ROM_QSTR(MP_QSTR_badge_type), MP_ROM_INT(BADGE_TYPE) },
};
static MP_DEFINE_CONST_DICT(p0tat0_globals, p0tat0_globals_table);

const mp_obj_module_t p0tat0_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *) &p0tat0_globals,
};

MP_REGISTER_MODULE(MP_QSTR__p0tat0, p0tat0_module);
