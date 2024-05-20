import os
from dataclasses import dataclass

from utils.files import uncompress_archive


@dataclass
class InstallProperties:
    identifiant: int
    file: str
    installed: bool = False


class InstallSysteme(object):

    @property
    def list_file(self):
        return self.__list_file

    @property
    def path_download(self):
        return self.__path_download

    @property
    def path_install(self):
        return self.__install_path

    def __init__(self, path_download, path_install):
        self.__path_download = path_download
        self.__path_download_archive = path_download + "/archive"
        self.__install_path = path_install
        self.__list_file = []
        self.__id = 0
        for file in os.listdir(self.__path_download):
            if os.path.isfile(
                os.path.join(self.__path_download, file)
            ):
                self.append_file(file)
        if not os.path.isdir(self.__path_download_archive):
            os.mkdir(self.__path_download_archive)
        else:
            for file in os.listdir(self.__path_download_archive):
                if os.path.isfile(
                    os.path.join(self.__path_download_archive, file)
                ):
                    self.append_file(file, True)

    def append_file(self, file_name, installed=False):
        file = InstallProperties(self.__id, file_name, installed)
        self.__list_file.append(file)
        self.__id += 1
        return file

    def remove_file(self, index):
        pass

    def remove_file_by_name(self, file_name):
        pass

    def get_file(self, file_name):
        file_exist = None
        for file in self.__list_file:
            if file_name == file.file:
                file_exist = file
                break

        return file_exist

    def install(self, file_installe):
        file = ""
        for file in self.__list_file:
            if file == file_installe:
                install_path = self.__install_path + "/" + file.file
                if not os.path.isdir(install_path):
                    os.mkdir(install_path)
                path_file = os.path.join(self.__path_download, file.file)
                error = uncompress_archive(
                    path_file,
                    os.path.join(
                        self.__install_path,
                        file.file
                    )
                )
                file.installed = not error
                if file.installed:
                    os.rename(
                        path_file,
                        self.__path_download_archive + "/" + file.file
                    )
                break
