import os

from utils.conf import ApllicationConfiguration
from utils.plugin_conf import PluginConfig
from utils.xdg import xdg_conf_path

from py_mod_manager.const import USER, PLUGIN

class CurrentGame(ApllicationConfiguration, PluginConfig):

    def __init__(self, current_game, auto_genrated=True):
        ApllicationConfiguration.__init__(self)

        self.__conf_path = xdg_conf_path()

        PluginConfig.__init__(self, current_game)
        if auto_genrated:
            self.set_current_game(current_game)
        else:
            self.__current_game = current_game

    @property
    def name(self):
        return self.__current_game.true_name

    @property
    def plugin_conf(self):
        return self.get_plugin_configuration("plugin_conf")

    @property
    def path_game(self):
        return self.get_plugin_configuration("path")

    @property
    def path_prefix(self):
        return self.get_plugin_configuration("prefix")

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
            copy = self.__current_game.copy
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

    @path_game.setter
    def path_game(self, value: str):
        self.set_configuration("path", value)
        self.save_plugin()

    @path_prefix.setter
    def path_prefix(self, value: str):
        self.set_configuration("prefix", value)
        print(value)
        self.save_plugin()

    @plugin_conf.setter
    def plugin_conf(self, value: bool):
        self.set_configuration("plugin_conf", value)
        self.save_plugin()

    def set_current_game(self, current_game):
        self.__current_game = current_game
        self._set_path(self.__current_game.name, self.__conf_path)
        if self._existe:
            self._load_plugin()
            if not self.__current_game.version == self.get_plugin_configuration("version"):
                print(f"ne correspond pas {self.__current_game.name}")
        else:
            self.set_configuration("version", self.__current_game.version)
            self.set_configuration("copy", self.__current_game.copy)
            self.set_configuration("archive", self.__current_game.archive)
            self.set_configuration("symbolic", self.__current_game.archive)
            self.save_plugin()

    def auto_detect_path_game(self, plugin, list_name_plugin):
        result = False
        prefix = ""
        install_dir = ""
        print("Auto detection", self._path)
        if self.get_plugin_configuration("path") == "":
            for game_name in self.__current_game.list_name:
                for plug in list_name_plugin:
                    plug = plugin.get_plugin_detect_game_by_name(plug)
                    print(plug, game_name)
                    game = plug.search_game(game_name)
                    install_dir = game.install_dir
                    if not install_dir == "":
                        prefix = game.prefix
                        result = True
                        break

        return result, prefix, install_dir




    def set_copy(self):
        self._default_force