#TODO Créer un système de chargement propre
#TODO Ajouter un systèmes de vérification de plugin

import os

from py_mod_manager.const import PKGDATADIR

from plugin_controller.plugin import PluginLoader
from plugin_controller.plugin_detect_game import PluginDetectGame
from plugin_controller.plugin_game import PluginGame

from utils.plugin_conf import PluginConfig
from utils.xdg import xdg_conf_path


def registery_game_plugin(module, list_module):
    list_module[module.PluginGames().name] = module.PluginGames

def registery_detect_game_plugin(module, list_module):
    list_module[module.PluginDetectGames().name] = module.PluginDetectGames

class PluginManager(object):
    def __init__(self):
        self.__path = xdg_conf_path()
        PLUGINS = "plugins"

        PLUGIN_GAMES = "PluginGames"
        PLUGIN_DETECT_GAMES = "PluginDetectGames"

        self.__plugins = dict()

        self.__CONF_PATH =  os.path.join(self.__path, "plugin_conf")

        self.__USER_PATH = os.path.join(self.__path, PLUGINS)
        self.__SYSTEME_PATH = os.path.join(PKGDATADIR, PLUGINS)

        self.__games = PluginLoader("games", PluginGame)
        self.__games.create_folder_plugin(self.__USER_PATH)
        self.__games.load(PLUGIN_GAMES, self.__SYSTEME_PATH, registery_game_plugin)
        self.__games.load(PLUGIN_GAMES, self.__USER_PATH, registery_game_plugin)

        self.__load_plugins(PLUGIN_GAMES, self.__games)

        self.__detect_games = PluginLoader("detect_games", PluginGame)
        self.__detect_games.create_folder_plugin(self.__USER_PATH)
        self.__detect_games.load(PLUGIN_DETECT_GAMES, self.__SYSTEME_PATH, registery_detect_game_plugin)
        self.__detect_games.load(PLUGIN_DETECT_GAMES, self.__USER_PATH, registery_detect_game_plugin)

    def __load_plugins(self, name, plugins):
        self.__plugins[name] = {"True" : dict(), "False": dict()}
        for plugin_name, plugin in plugins.get_liste_plugins().items():
            conf = PluginConfig(plugin())
            conf.set_path_plugin(plugin_name, self.__path)
            if not conf.existe:
                conf.save_plugin()
            conf.load_plugin()
            self.__plugins[name][str(conf.is_enable())][plugin_name] = plugin

    def list_name_plugin_load_enabled(plugin):
        return self.__plugins[plugin]["True"].clone()

    def list_name_plugin_load_disable(plugin):
        return self.__plugins[plugin]["false"].clone()

    def list_plugin(plugin)
        list_plugin = self.__plugins

    @property
    def CONF_PATH(self):
        return self.__CONF_PATH

    @property
    def USER_PATH(self):
        return self.__USER_PATH

    @property
    def SYSTEME_PATH(self):
        return self.__SYTEME_PATH
