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
        self._locals_path = [os.path.join('steam',self.STEAMAPPS), os.path.join('.steam', self.STEAMAPPS)]
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

    def detect_prefix(self, appid):
        for i in range(len(self.__detect_game_path)):
            try:
                path = os.path.join(self.__detect_game_path[i], self.STEAMAPPS )
                path = os.path.join(path, "compatdata")
                for file_name in os.listdir(path):
                    if file_name == appid:
                        self._prefix = os.path.join(path, appid)
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
                        self._game_name = d['AppState']['name']
                        self.detect_prefix(d['AppState']['appid'])
                        self._install_dir = d['AppState']['installdir']
                        print(self._install_dir)

    def _search_game(self):
        self.detect_path(os.path.join(self.flatpak_base_path, self._flatpak_path))
        for i in range(len(self.__detect_game_path)):
            self.detect_game(os.path.join(self.base_path, self.__detect_game_path[i]))