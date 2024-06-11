import argparse
import hashlib
import io
import os
import sys
import tarfile

parser = argparse.ArgumentParser(
    prog='package.py',
    description='Package the payload directory ready for building into the firmware'
)

parser.add_argument('directory', help='The directory to package')
parser.add_argument('outfile', help='The output file')


def filter_py(tarinfo: tarfile.TarInfo):
    print(f"AAA {tarinfo.name}")
    if os.path.splitext(tarinfo.name)[1] != ".py":
        return None

    return tarinfo


def write_bytes(f, name, data):
    f.write(f"const uint8_t {name}[] = {{\n")

    while len(data) > 0:
        chunk = data[:16]
        data = data[16:]
        f.write("    ")
        f.write(", ".join(f'0x{b:02x}' for b in chunk))
        f.write(",\n")
    f.write("};\n")


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        sys.stderr.write("First argument is not a directory.\n")
        sys.exit(1)

    file_buffer = io.BytesIO()
    tar = tarfile.open(
        fileobj=file_buffer,
        mode='w:gz',
        dereference=True,
        format=tarfile.GNU_FORMAT,
    )

    for root, dirs, files in os.walk(args.directory):
        for name in dirs:
            dir = os.path.join(root, name)
            tar.add(dir, arcname=os.path.relpath(dir, start=args.directory), recursive=False)
        for name in files:
            if os.path.splitext(name)[1] == ".py":
                file = os.path.join(root, name)
                tar.add(file, arcname=os.path.relpath(file, start=args.directory))

    tar.close()

    with open(args.outfile, 'w') as f:
        data = file_buffer.getvalue()

        f.write("// Auto-generated by package.py\n")
        f.write("#include <stddef.h>\n")
        f.write("#include <stdint.h>\n")
        f.write("\n")
        f.write(f"const size_t fri3d_application_length = {len(data)};\n")
        write_bytes(f, 'fri3d_application_digest', hashlib.md5(data).digest())
        write_bytes(f, 'fri3d_application_data', data)

    file_buffer.close()

    sys.exit(0)
