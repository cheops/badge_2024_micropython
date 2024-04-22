from esp32 import NVS
import toml

from fri3d import logging

log = logging.Log(__name__, level=logging.INFO)

def key_size(key):
    return key + ".size"

def key_blob(key):
    return key + ".blob"

def read_blob(label, key):
    nvs_area = NVS(label)
    try:
        size = nvs_area.get_i32(key_size(key))
        blob = bytearray(size)
        nvs_area.get_blob(key_blob(key), blob)
    except OSError as e:
        if e.errno == -4354 or e.errno == -4364:  # ESP_ERR_NVS_NOT_FOUND or ESP_ERR_NVS_INVALID_LENGTH
            blob = bytearray(0)
        else:
            raise e
    return blob

def write_blob(label, key, blob):
    nvs_area = NVS(label)
    nvs_area.set_i32(key_size(key), len(blob))
    nvs_area.set_blob(key_blob(key), blob)
    nvs_area.commit()

def toml_blob_to_dict(blob):
    d = blob.decode('utf-8')
    return toml.loads(d)

def dict_to_toml_blob(d):
    s = toml.dumps(d)
    return s.encode('utf-8')
