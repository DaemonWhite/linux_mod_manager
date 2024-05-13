import os
from dataclasses import dataclass

from utils.files import uncompress_archive


@dataclass
class InstallProperties:
    identifiant: int
    file: str


class InstallSysteme(object):

    def __init__(self, path_download, path_install):
        self.__path_download = path_download
        self.__install_path = path_install
        self.__list_file = []
        index = 0
        for file in os.listdir(self.__path_download):
            if os.path.isfile(
                os.path.join(self.__path_download, file)
            ):
                self.__list_file.append(InstallProperties(
                    index,
                    file
                ))
                index += 1

    def existed(self, identifiant):
        existe = False
        for i, file in enumerate(self.__list_file):
            if identifiant == file.identifiant:
                existe = True
                break

        return existe

    def install(self, identifiant):
        file = ""
        for file in self.__list_file:
            if file.identifiant == identifiant:
                install_path = self.__install_path + "/" + file.file
                if not os.path.isdir(install_path):
                    os.mkdir(install_path)

                uncompress_archive(
                    os.path.join(
                        self.__path_download,
                        file.file
                    ),
                    os.path.join(
                        self.__install_path,
                        file.file
                    )
                )
                break

    def no_installed(self):
        return self.__list_file
