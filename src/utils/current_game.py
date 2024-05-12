import os

from utils.xdg import xdg_conf_path
from utils.files import generate_dict_archive, lower_case_recursif

from py_mod_manager.const import USER, PLUGIN


class CurrentGame(object):

    def __init__(self, settings):

        self.__conf_path = xdg_conf_path()
        self.__settings = settings
        self.__current_game = None
        self.__current_config = None

    @property
    def name(self):
        return self.__current_game.true_name

    @property
    def plugin_name(self):
        return self.__current_game.name

    @property
    def conflit_syst(self):
        return self.__current_config.conflit_syst

    @property
    def post_conf(self):
        return self.__current_config.post_conf

    @property
    def plugin_conf(self):
        return self.__current_config.get_plugin_configuration("plugin_conf")

    @property
    def path_game(self):
        return self.__current_config.get_plugin_configuration("path")

    @property
    def path_prefix(self):
        return self.__current_config.get_plugin_configuration("prefix")

    @property
    def symbolic(self):
        symbolic = False
        mode_symb = self.__settings.get_mode_symb()
        if mode_symb == USER:
            symbolic = self.__current_config.get_plugin_configuration(
                "symbolic"
            )
        elif mode_symb == PLUGIN:
            symbolic = self.__current_game.symbolic
        else:
            symbolic = self.__settings.get_app_symb()
        return symbolic

    @property
    def copy(self):
        copy = False
        mode_copy = self.__settings.get_mode_copy()
        if mode_copy == USER:
            copy = self.__current_config.get_plugin_configuration("copy")
        elif mode_copy == PLUGIN:
            copy = self.__current_game.copy
        else:
            copy = self.__settings.get_app_copy()
        return copy

    @property
    def archive(self):
        archive = False
        mode_archive = self.__settings.get_mode_archive()
        if mode_archive == USER:
            archive = self.__current_config.get_plugin_configuration("archive")
        elif mode_archive == PLUGIN:
            archive = self.__current_game.archive
        else:
            archive = self.__settings.get_app_archive()
        return archive

    @property
    def systeme(self):
        return self.__current_game.systeme

    @path_game.setter
    def path_game(self, value: str):
        self.__current_config.set_configuration("path", value)
        self.save_plugin()

    @path_prefix.setter
    def path_prefix(self, value: str):
        self.__current_config.set_configuration("prefix", value)
        self.save_plugin()

    @plugin_conf.setter
    def plugin_conf(self, value: bool):
        self.__current_config.set_configuration("plugin_conf", value)
        self.save_plugin()

    def set_configuration(self, name, info):
        self.__current_config.set_configuration(name, info)

    def set_current_game(self, current_game, current_config):
        self.__current_game = current_game
        self.__current_config = current_config
        self.__current_config.set_path_plugin(
            self.__current_game.name,
            self.__conf_path
        )
        if not self.__current_game.version == self.__current_config.get_plugin_configuration("version"):
            print(f"ne correspond pas {self.__current_game.name}")

    def post_traitement(self):
        result = True
        try:
            lower_case_recursif(self.path_game)
            if not self.__current_game.post_traitement():
                return False
            self.__current_config.enable_post_conf(True)
        except Exception as e:
            self.__current_config.enable_post_conf(False)
            print("Error poste traitement : ", e)
            result = False
        return result

    def init_conflit_syst(self):
        result = True
        try:
            generate_dict_archive(False, self.path_game)
            self.__current_config.enable_init_conflit_syst(True)
        except Exception as e:
            self.__current_config.enable_init_conflit_syst(False)
            print("Error dict traitement : ", e)
            result = False
        return result

    def save_plugin(self):
        self.__current_config.save_plugin()

    def auto_detect_path_game(self, plugin, list_name_plugin):
        result = False
        if self.__current_config.get_plugin_configuration("path") == "":
            for game_name in self.__current_game.list_name:
                for plug_name, plugin_detect in list_name_plugin.items():
                    if plugin_detect[1].is_enable():
                        plug = plugin_detect[0]()
                        game = plug.search_game(game_name)
                        if not game.install_dir == "":
                            self.path_game = game.install_dir
                            self.path_prefix = game.prefix
                            result = True
                            break
        return result

    def set_copy(self):
        self._default_force
