from gi.repository import GLib

from plugin_controller.plugin_base import PluginBase
from pathlib import Path
import os

class GameData(object):
    def __init__(self):
        self.name = str()
        self.prefix = str()
        self.install_dir = str()

class PluginDetectGame(PluginBase):

    def __init__(self, name, version, plugin_version):
        super().__init__(name, version, plugin_version, 'detect_games')
        self.__base_path = Path.home()
        self.__flatpak_base_path = f"{Path.home()}/.var/app"
        self._flatpak_path = ""
        self._locals_path = [str()]
        self._absolute_path = [str()]
        self._flatpak = False
        self._local = False
        self._windows = False
        self._game = str()
        self.__game = GameData()

    @property
    def _game_name(self):
        return self.__game.name
    @property
    def _prefix(self):
        return self.__game.prefix
    @property
    def _install_dir(self):
        return self.__game.install_dir

    @property
    def flatpak_base_path(self):
        return self.__flatpak_base_path

    @property
    def base_path(self):
        return self.__base_path

    @property
    def flatpak(self):
        return self._flatpak

    @property
    def local(self):
        return self._local

    @property
    def windows(self):
        return self._windows

    @property
    def flatpak_path(self):
        return self._flatpak_path

    @property
    def locals_path(self):
        return self._locals_path

    @_game_name.setter
    def _game_name(self, name):
        self.__game.name = name

    @_prefix.setter
    def _prefix(self, prefix):
        self.__game.prefix = prefix

    @_install_dir.setter
    def _install_dir(self, install_dir):
        self.__game.install_dir = install_dir

    def _search_game(self):
        pass

    def search_game(self, game):
        self._game = game
        self._search_game()
        return self.__game
