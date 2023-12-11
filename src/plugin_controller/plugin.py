import importlib
import os

class PluginLoader(object):

    def __init__(self, NAME_PLUGIN, MODULE):
        self.__NAME_PLUGIN = NAME_PLUGIN
        self.__MODULE = MODULE
        self.__list_plugin = dict()

    @property
    def NAME_PLUGIN(self):
        return self.__NAME_PLUGIN

    def create_folder_plugin(self, folder):
        path = os.path.join(folder, self.__NAME_PLUGIN)
        if not os.path.isdir(path):
            os.makedirs(path)

    def load(self, name, path, registery_plugin):
        folder = os.path.join(path, self.__NAME_PLUGIN)
        try:
            for file_name in os.listdir(folder):
                if file_name.endswith(".py") and file_name != "__init__.py":
                    plugin_name = os.path.splitext(file_name)[0]
                    spec = importlib.util.spec_from_file_location(name, f"{folder}/{file_name}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    registery_plugin(module, self.__list_plugin)
        except Exception as e:
            print(f"Impossible d'accéder au donné {folder} \n\n {e}")

    def get_liste_plugins(self):
        return self.__list_plugin.copy()

    def unload(self):
        self.__list_plugin = dict()

class PluginManager(object):
    GAME = "games"
    DETECT_GAMES = "detect_games"
    def __init__(self, path, user_path):
        self.__folder_path = path
        self.__user_folder_path = os.path.join(user_path, "plugin")

        self.__plugins_game = dict()
        self.__plugin_detect = dict()

    @staticmethod
    def verif_folder(folder, target):
        path = os.path.join(folder, target)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    @staticmethod
    def __load(name, detect_plugin_name, list_module, folder):
        try:
            for file_name in os.listdir(folder):
                if file_name.endswith(".py") and file_name != "__init__.py":
                    plugin_name = os.path.splitext(file_name)[0]
                    spec = importlib.util.spec_from_file_location(name, f"{folder}/{file_name}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    list_module[detect_plugin_name(module)] = module
        except Exception as e:
            print(f"Impossible d'accéder au donné {folder} \n\n {e}")


    def load_detect_plugin(self):
        name = 'PluginDetectGames'
        def plugin_name(module):
            return module.PluginDetectGames().name

        sys_path = self.verif_folder(self.__folder_path, self.DETECT_GAMES)
        user_path = self.verif_folder(self.__user_folder_path, self.DETECT_GAMES)
        self.__load(name, plugin_name, self.__plugin_detect, sys_path)
        self.__load(name, plugin_name, self.__plugin_detect, user_path)

    def load_games(self):
        name = 'PluginGames'
        def plugin_name(module):
            return module.PluginGames().name

        sys_path = self.verif_folder(self.__folder_path, self.GAME)
        user_path = self.verif_folder(self.__user_folder_path, self.GAME)
        self.__load(name, plugin_name, self.__plugins_game, sys_path)
        self.__load(name, plugin_name, self.__plugins_game, user_path)

    def get_first_plugin_game(self):
        plugin = None
        for _, plug in self.__plugins_game.items():
            plugin = plug
            break
        return  plugin.PluginGames()

    def get_plugin_detect_game_by_name(self, name):
        return self.__plugin_detect[name].PluginDetectGames()

    def get_plugin_game_by_name(self, name):
        return self.__plugins_game[name].PluginGames()

    def get_list_plugin_detect_game(self):
        list_plugin = list()
        for _, plugin in self.__plugin_detect.items():
            list_plugin.append(plugin.PluginDetectGames().name)

        return list_plugin

    def get_list_plugin_game(self):
        list_plugin = list()
        for _, plugin in self.__plugins_game.items():
            list_plugin.append(plugin.PluginGames().name)

        return list_plugin
