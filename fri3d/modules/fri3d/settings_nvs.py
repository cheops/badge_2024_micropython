from esp32 import NVS
import toml

def key_size(key):
    return key + ".size"

def key_blob(key):
    return key + ".blob"

def read_blob(label, key):
    nvs_area = NVS(label)
    size = nvs_area.get_i32(key_size(key))
    blob = bytearray(size)
    nvs_area.get_blob(key_blob(key), blob)
    return blob

def write_blob(label, key, blob):
    nvs_area = NVS(label)
    nvs_area.set_i32(key_size(key), len(blob))
    nvs_area.set_blob(key_blob(key), blob)
    nvs_area.commit()

def toml_blob_to_dict(blob):
    d = blob.decode('utf-8')
    return toml.loads(dec)

def dict_to_toml_blob(d):
    s = toml.dumps(d)
    return s.encode('utf-8')
