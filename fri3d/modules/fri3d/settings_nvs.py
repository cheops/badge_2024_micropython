import nvs
from fri3d import toml

def read_blob(label, key):
    """return the blob for nvs partition with label and key
    
    exception OSError: (-4354, 'ESP_ERR_NVS_NOT_FOUND') when the key is not found in the partition

    try:
        b = read_blob(label, key)
    except OSError as e:
        if e.errno == -4354:
            print(f"no blob found for {key}")
    """
    nvs_area = nvs.NVS(label)
    return nvs_area.get(nvs.TYPE_BLOB, key)

def write_blob(label, key, blob):
    "write blob to nvs partition label with key"
    nvs_area = nvs.NVS(label)
    nvs_area.set(nvs.TYPE_BLOB, key, blob)
    nvs_area.commit()

def toml_blob_to_dict(blob):
    d = blob.decode('utf-8')
    return toml.loads(d)

def dict_to_toml_blob(d):
    s = toml.dumps(d)
    return s.encode('utf-8')