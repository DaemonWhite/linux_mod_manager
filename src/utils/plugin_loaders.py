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

        self.__PLUGIN_GAMES = "PluginGames"
        self.__PLUGIN_DETECT_GAMES = "PluginDetectGames"

        self.__plugins = dict()

        self.__CONF_PATH =  os.path.join(self.__path, "plugin_conf")

        self.__USER_PATH = os.path.join(self.__path, PLUGINS)
        self.__SYSTEME_PATH = os.path.join(PKGDATADIR, PLUGINS)

        self.__load()



    def __load(self):
        self.__games = PluginLoader("games", PluginGame)
        self.__games.create_folder_plugin(self.__USER_PATH)
        self.__games.load(self.__PLUGIN_GAMES, self.__SYSTEME_PATH, registery_game_plugin)
        self.__games.load(self.__PLUGIN_GAMES, self.__USER_PATH, registery_game_plugin)

        self.__load_plugins(self.__PLUGIN_GAMES, self.__games)

        self.__detect_games = PluginLoader("detect_games", PluginDetectGame)
        self.__detect_games.create_folder_plugin(self.__USER_PATH)
        self.__detect_games.load(self.__PLUGIN_DETECT_GAMES, self.__SYSTEME_PATH, registery_detect_game_plugin)
        self.__detect_games.load(self.__PLUGIN_DETECT_GAMES, self.__USER_PATH, registery_detect_game_plugin)
        self.__load_plugins(self.__PLUGIN_DETECT_GAMES, self.__detect_games)

    def reload(self):
        self.__plugins.clear()
        self.__load()


    def __load_plugins(self, name, plugins):
        self.__plugins[name] = dict()
        for plugin_name, plugin in plugins.get_liste_plugins().items():
            conf = PluginConfig(plugin())
            conf.set_path_plugin(plugin_name, self.__path)
            if not conf.existe:
                conf.save_plugin()
            conf.load_plugin()
            self.__plugins[name][plugin_name] = (plugin, conf)


    def get_list_all_plugin(self):
        return self.__plugins

    def get_list_plugin(self, plugin):
        print(plugin)
        return self.__plugins[plugin]

    def get_plugin(self, plugin, plugin_name):
        return self.__plugins[plugin][plugin_name][0]()

    def get_conf_plugin(self, plugin, plugin_name):
        return self.__plugins[plugin][plugin_name][1]

    @property
    def CONF_PATH(self):
        return self.__CONF_PATH

    @property
    def USER_PATH(self):
        return self.__USER_PATH

    @property
    def SYSTEME_PATH(self):
        return self.__SYTEME_PATH

    @property
    def PLUGIN_GAMES(self):
        return self.__PLUGIN_GAMES

    @property
    def PLUGIN_DETECT_GAMES(self):
        return self.__PLUGIN_DETECT_GAMES
