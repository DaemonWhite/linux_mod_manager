from plugin_controller.plugin_detect_game import PluginDetectGame

import os
import json

import vdf

from pathlib import PurePath, Path

class PluginDetectGames(PluginDetectGame):

    def __init__(self,):
        super().__init__('Heroic', 1, 0.1)
        self.__detect_game_path = []
        self._local = True
        self._flatpak = False
        self._locals_path = '.config/heroic'
        self._flatpak_path = "com.heroicgameslauncher.hgl/config"

    def detect_game(self, path, installed_json):
        game_name = str()
        for game in installed_json:
            game_name = installed_json[game]["title"]
            if game_name == self._game and not installed_json[game]["is_dlc"]:
                self._game_name = game_name
                self._install_dir = installed_json[game]["install_path"]
                game_config = "GamesConfig/" + installed_json[game]["app_name"] + ".json"
                print(game_config)
                with open(os.path.join(path, game_config), "r") as json_file:
                    self._prefix = json.load(json_file)[game]["winePrefix"]

    def _search_game(self):
        flatpak = os.path.join(self.flatpak_base_path, self._flatpak_path)
        local = os.path.join(self.base_path, self._locals_path)
        paths = []
        if os.path.isdir(flatpak):
            paths += [flatpak]
        if os.path.isdir(local):
            paths += [local]
        for path in paths:
            installed_path = os.path.join(path, "legendaryConfig/legendary/installed.json")
            with open(installed_path, "r") as json_file:
                self.detect_game(path, json.load(json_file))
