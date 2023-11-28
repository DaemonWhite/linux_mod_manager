import os

from utils.conf import ApllicationConfiguration
from utils.plugin_conf import PluginConfig
from utils.xdg import xdg_conf_path

from py_mod_manager.const import USER, PLUGIN

class CurrentGame(ApllicationConfiguration, PluginConfig):

    def __init__(self, current_game):
        ApllicationConfiguration.__init__(self)

        self.__conf_path = xdg_conf_path()

        PluginConfig.__init__(self)

        self.set_current_game(current_game)



    @property
    def symbolic(self):
        symbolic = False
        if self._mode_symb == USER:
            symbolic = self.get_plugin_configuration("symbolic")
        elif self._mode_symb == PLUGIN:
            symbolic = self.__current_game.symbolic
        else:
            symbolic = self.get_app_symb()
        return symbolic

    @property
    def copy(self):
        copy = False
        if self._mode_copy == USER:
            copy = self.get_plugin_configuration("copy")
        elif self._mode_copy == PLUGIN:
            copy = self.__current_game.copie
        else:
            copy = self.get_app_copy()
        return copy

    @property
    def archive(self):
        archive = False
        if self._mode_archive == USER:
            archive = self.get_plugin_configuration("archive")
        elif self._mode_archive == PLUGIN:
            archive = self.__current_game.archive
        else:
            archive = self.get_app_archive()
        return archive

    @property
    def systeme(self):
        return self.__current_game.systeme

    def set_current_game(self, current_game):
        self.__current_game = current_game
        self._set_path(self.__current_game.name, self.__conf_path)
        if self._existe:
            self._load_plugin()
            if not self.__current_game.version == self.get_plugin_configuration("version"):
                print("ne correspond pas")
        else:
            self.set_configuration("version", self.__current_game.version)
            self.set_configuration("copy", self.__current_game.copie)
            self.set_configuration("archive", self.__current_game.archive)
            self.set_configuration("symbolic", self.__current_game.archive)
            self.save_plugin()

    def set_copy(self):
        self._default_force