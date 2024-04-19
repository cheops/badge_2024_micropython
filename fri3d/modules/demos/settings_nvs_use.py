from fri3d.settings_nvs import write_blob, read_blob, dict_to_toml_blob, toml_blob_to_dict

settings = {
    'aps': [
        {'ssid': 'your-ssid', 'key': 'your-key'},
        {'ssid': 'fri3d_badge', 'key': 'fri3d_2024'}
        ]
    }

print(settings)

write_blob('system', 'wifi', dict_to_toml_blob(settings))

settings_2 = toml_blob_to_dict(read_blob('system', 'wifi'))

print(settings_2)