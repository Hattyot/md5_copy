import hashlib
import argparse
import os
import shutil


def file_checksum(file):
    with open(file, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def checksum_check(source, destination):
    if os.path.exists(destination):
        source_md5 = file_checksum(source)
        destination_md5 = file_checksum(destination)
        if source_md5 == destination_md5:
            return True


def copytree(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
        shutil.copystat(source, destination)

    lst = os.listdir(source)

    for item in lst:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isdir(source_path):
            copytree(source_path, destination_path)
        elif checksum_check(source_path, destination_path):
            continue
        else:
            shutil.copy2(source_path, destination_path)


parser = argparse.ArgumentParser()

parser.add_argument('-s', help='source folder')
parser.add_argument('-d', help='destination folder')

if __name__ == '__main__':
    args = parser.parse_args()
    source_folder = os.path.abspath(args.s)
    destination_folder = os.path.abspath(args.d)
    copytree(source_folder, destination_folder)
