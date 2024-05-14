import os
from dataclasses import dataclass

from utils.files import uncompress_archive


@dataclass
class InstallProperties:
    identifiant: int
    file: str
    installed: bool = False


class InstallSysteme(object):

    def __init__(self, path_download, path_install):
        self.__path_download = path_download
        self.__install_path = path_install
        self.__list_file = []
        self.__id = 0
        for file in os.listdir(self.__path_download):
            if os.path.isfile(
                os.path.join(self.__path_download, file)
            ):
                self.append_file(file)

    def append_file(self, file):
        file = InstallProperties(self.__id, file)
        self.__list_file.append(file)
        self.__id += 1
        return file

    def existed(self, identifiant):
        existe = False
        for i, file in enumerate(self.__list_file):
            if identifiant == file.identifiant:
                existe = True
                break

        return existe

    def install(self, file_installe):
        file = ""
        for file in self.__list_file:
            if file == file_installe:
                install_path = self.__install_path + "/" + file.file
                if not os.path.isdir(install_path):
                    os.mkdir(install_path)

                error = uncompress_archive(
                    os.path.join(
                        self.__path_download,
                        file.file
                    ),
                    os.path.join(
                        self.__install_path,
                        file.file
                    )
                )
                file.installed = not error
                break

    def no_installed(self):
        return self.__list_file
