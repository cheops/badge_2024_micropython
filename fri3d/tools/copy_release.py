#!/usr/bin/env python
#
# from the root of this repository
#
# python fri3d/tools/copy_release.py
# python fri3d/tools/copy_release.py --badge_type 2022
#
import os
import argparse
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

parser = argparse.ArgumentParser(
    prog='copy_release.py',
    description='Copy a prebuild release from this repository to the fri3d-ota repository',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument('--badge_type', help="Which badge type", choices=['2022', '2024'], default='2024')
parser.add_argument('--dest_repo', help="Destination Repository", default='../cheops_fri3d-ota')

PORT_DIR = "ports/esp32"


def create_flash_args_content(badge_type):
    if badge_type == '2022':
        return _create_flash_args_content_2022()
    elif badge_type == '2024':
        return _create_flash_args_content_2024()
    else:
        raise Exception("unsupported badge_type")


def _create_flash_args_content_2022():
    return """--before default_reset --after hard_reset --chip esp32  write_flash --flash_mode dio --flash_size 16MB --flash_freq 40m 
0x1000 bootloader.bin
0x8000 partition-table.bin
0x1d000 ota_data_initial.bin
0x30000 micropython.bin"""


def _create_flash_args_content_2024():
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
    
    args = parser.parse_args()
    
    print(f"{PORT_DIR=}")
    BUILD_DIR = os.path.join(PORT_DIR, f'build-FRI3D_BADGE_{args.badge_type}')
    print(f"{BUILD_DIR=}")
    print(f"{args.dest_repo=}")
    
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
    
    if args.badge_type == '2022':
        to_copy.remove('micropython.uf2')
    
    dest_dir = os.path.join(args.dest_repo, 'ota', f'fri3d_badge_{args.badge_type}', version)
    os.makedirs(dest_dir, exist_ok=True)
    
    for f in to_copy:
        src = os.path.join(BUILD_DIR, f)
        print(f"copying {src} to {os.path.join(dest_dir, os.path.basename(f))}")
        shutil.copy2(src, dest_dir)
    
    flash_args = os.path.join(dest_dir, 'flash_args')
    print(f"creating {flash_args}")
    with open(flash_args, 'w') as f:
        f.write(create_flash_args_content(args.badge_type))
    
    create_flashable_zip(dest_dir, f'fri3d_badge_{args.badge_type}', version)


if __name__ == "__main__":
    main()
