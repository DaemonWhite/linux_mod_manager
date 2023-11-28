import os
import xdg.BaseDirectory

from utils.conf import ApllicationConfiguration
from utils.plugin_conf import PluginConfig

class CurrentGame(ApllicationConfiguration, PluginConfig):

    def __init__(self, current_game):
        ApllicationConfiguration.__init__(self)
        conf_path = "~"

        try:
            conf_path = xdg.BaseDirectory.xdg_config_home
        except:
            print("Error no XDG Conf define")

        self.__conf_path = os.path.join(conf_path, "linux_mode_manager")

        if not os.path.isdir(self.__conf_path):
            os.makedirs(self.__conf_path)

        PluginConfig.__init__(self)

        self.set_current_game(current_game)



    @property
    def symbolic(self):
        symbolic = False
        if self._mode_symb == 0:
            symbolic = self.get_plugin_configuration("symbolic")
        elif self._mode_symb == 1:
            symbolic = self.__current_game.symbolic
        else:
            symbolic = self.get_app_symb()
        return symbolic

    @property
    def copy(self):
        copy = False
        if self._mode_copy == 0:
            copy = self.get_plugin_configuration("copy")
        elif self._mode_copy == 1:
            copy = self.__current_game.copie
        else:
            copy = self.get_app_copy()
        return copy

    @property
    def archive(self):
        archive = False
        if self._mode_archive == 0:
            archive = self.get_plugin_configuration("archive")
        elif self._mode_archive == 1:
            archive = self.__current_game.archive
        else:
            archive = self.get_app_archive()
        return archive

    @property
    def systeme(self):
        return self.__current_game.systeme

    def set_current_game(self, current_game):
        self.__current_game = current_game
        self._set_path(self.__current_game.name_game, self.__conf_path)
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