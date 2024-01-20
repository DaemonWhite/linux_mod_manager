from plugin_controller.plugin_detect_game import PluginDetectGame

import vdf
import os
from pathlib import PurePath, Path

class PluginDetectGames(PluginDetectGame):
    STEAMAPPS = 'steamapps'

    def __init__(self,):
        super().__init__('Steam', 1, 0.1)
        self.__detect_game_path = []
        self._local = True
        self._flatpak = True
        self._locals_path = [os.path.join('steam',self.STEAMAPPS), os.path.join('.steam/steam', self.STEAMAPPS)]
        self._flatpak_path = "com.valvesoftware.Steam/data/Steam/" + self.STEAMAPPS

    def detect_path(self, path):
        if not os.path.isdir(path):
            return
        for file_name in os.listdir(path):
            if file_name.endswith(".vdf"):
                d = vdf.load(open(os.path.join(path, file_name)))
                nb_path = int(len(d['libraryfolders']))
                for index in range(nb_path):
                    self.__detect_game_path.append(d['libraryfolders'][f'{index}']['path'])

    def detect_folder(self, path_to_find, data_path):
        for i in range(len(self.__detect_game_path)):
            try:
                path = os.path.join(self.__detect_game_path[i], self.STEAMAPPS )
                path = os.path.join(path, data_path)
                for file_name in os.listdir(path):
                    if file_name == path_to_find:
                        return os.path.join(path, path_to_find)
            except Exception as e:
                print(f"Chemin non trouver {e}")


    def detect_game(self, path):
        path = os.path.join(path, self.STEAMAPPS)
        if not os.path.isdir(path):
            return

        for file_name in os.listdir(path):
            if file_name.endswith(".acf"):
                    d = vdf.load(open(os.path.join(path, file_name)))
                    name = d['AppState']['name']
                    if name == self._game:
                        self._game_name = name
                        self._prefix = self.detect_folder(d['AppState']['appid'], 'compatdata')
                        self._install_dir =  self.detect_folder(d['AppState']['installdir'], 'common')

    def _search_game(self):
        # Search flatpak
        self.detect_path(os.path.join(self.flatpak_base_path, self._flatpak_path))
        # Search in local

        for path in self._locals_path:
            print(path)
            self.detect_path(os.path.join(self.base_path, path))

        for i in range(len(self.__detect_game_path)):
            self.detect_game(os.path.join(self.base_path, self.__detect_game_path[i]))
