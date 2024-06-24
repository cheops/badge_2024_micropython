#!/usr/bin/env python
import os
import shutil
from zipfile import ZIP_DEFLATED, ZipFile


PORT_DIR = "ports/esp32"
BUILD_DIR = os.path.join(PORT_DIR, 'build-FRI3D_BADGE_2024')
DEST_REPO = '../cheops_fri3d-ota'


def create_flash_args_content():
    return """--before default_reset --after no_reset --chip esp32s3  write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m 
0x0 bootloader.bin
0x8000 partition-table.bin
0x1d000 ota_data_initial.bin
0x30000 micropython.bin"""


def get_version_from_file(version_file):
    "looks for version = '<version_str>' in file and returns version_str"
    version = ''
    with open(version_file, 'r') as lines:
        for line in lines:
            if line.find('version') != -1:
                s = line.rstrip().split('=')
                v = s[1].strip()
                version = v.strip("'\"")
                break
    return version
                

def create_flashable_zip(dest_dir, board_name, version):
    zip_name = f"{board_name}-{version}.zip"
    zip_full_name = os.path.join(dest_dir, zip_name)

    print(f"creating zip {zip_full_name}")

    to_zip = [
        'flash_args',
        'bootloader.bin', 
        'micropython.bin', 
        'ota_data_initial.bin', 
        'partition-table.bin']

    with ZipFile(zip_full_name, 'w', ZIP_DEFLATED) as zf:
        for t in to_zip:
            zf.write(os.path.join(dest_dir, t), t)


def main():

    print(f"{PORT_DIR=}")
    print(f"{BUILD_DIR=}")
    print(f"{DEST_REPO=}")

    version_file = 'fri3d/fri3d_application/src/payload/fri3d/version.py'
    version = get_version_from_file(version_file)
    print(f"{version=}")

    to_copy = [
        'bootloader/bootloader.bin', 
        'bootloader/bootloader.elf', 
        'bootloader/bootloader.map', 
        'firmware.bin', 
        'micropython.bin', 
        'micropython.elf', 
        'micropython.map', 
        'micropython.uf2', 
        'ota_data_initial.bin', 
        'partition_table/partition-table.bin']

    dest_dir = os.path.join(DEST_REPO, 'ota', 'fri3d_badge_2024', version)
    os.makedirs(dest_dir, exist_ok=True)

    for f in to_copy:
        src = os.path.join(BUILD_DIR, f)
        print(f"copying {src} to {os.path.join(dest_dir, os.path.basename(f))}")
        shutil.copy2(src, dest_dir)
    
    flash_args = os.path.join(dest_dir, 'flash_args')
    print(f"creating {flash_args}")
    with open(flash_args, 'w') as f:
        f.write(create_flash_args_content())
    
    create_flashable_zip(dest_dir, 'fri3d_badge_2024', version)


if __name__ == "__main__":
    main()
