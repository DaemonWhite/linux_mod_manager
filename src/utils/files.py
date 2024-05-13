import os
import hashlib

import zipfile
import py7zr
import rarfile

from gi.repository import Gio


def slice_path_in_file(path):
    slice_index = path.rfind('/') + 1
    return path[slice_index:]


def sha256_checksum(file):
    SIZE_BLOC = 65536
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        for bloc in iter(lambda: f.read(SIZE_BLOC), b''):
            sha256.update(bloc)
    return sha256.hexdigest()


def lower_case_recursif(path):
    dirs = os.listdir(path)
    for file_and_folder in dirs:
        new_path = os.path.join(path, file_and_folder.lower())
        os.rename(
            os.path.join(path, file_and_folder),
            os.path.join(new_path)
        )
        if os.path.isdir(os.path.join(new_path)):
            lower_case_recursif(new_path)


def generate_dict_archive(activate_hash=False, path="/", prefix="/"):
    archive = {}
    dirs = os.listdir(path)
    files = []
    folders = []
    for file in dirs:
        path_file = os.path.join(path, file)
        if os.path.isfile(path_file):
            file_hash = -1
            if activate_hash:
                file_hash = sha256_checksum(path_file)

            files.append((file_hash, file))

    for folder in dirs:
        if os.path.isdir(os.path.join(path, folder)):
            folders.append(
                generate_dict_archive(
                    activate_hash,
                    os.path.join(path, folder),
                    folder
                )
            )

    archive[prefix] = {'files': files, 'folders': folders}
    return archive


def unzip_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def unzip_7zip(file_path, extract_to):
    with py7zr.SevenZipFile(file_path, mode='r') as z:
        z.extractall(path=extract_to)


def unrar(file_path, extract_to):
    with rarfile.RarFile(file_path, 'r') as rf:
        rf.extractall(extract_to)


def uncompress_archive(path_file, path_dest):
    file = Gio.file_new_for_path(path_file)
    info = file.query_info(
        'standard::content-type',
        Gio.FileQueryInfoFlags.NONE,
        None
    )

    print(path_file)
    print(info.get_content_type())

    if info.get_content_type().find("7z") >= 0:
        unzip_7zip(path_file, path_dest)
    elif info.get_content_type().find("rar") >= 0:
        unrar(path_file, path_dest)
    elif info.get_content_type().find("zip") >= 0:
        unzip_zip(path_file, path_dest)
    # elif info.get_content_type().find("tar") >= 0:
    #     pass
    else:
        print("Format d'archive non pris en charge.")

