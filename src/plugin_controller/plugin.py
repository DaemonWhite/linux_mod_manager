import importlib
import os

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
                    print(module)
                    list_module[detect_plugin_name(module)] = module
        except Exception:
            print(f"Impossible d'accéder au donné {folder}")


    def load_detect_plugin():
        name = 'DetectGames'
        def plugin_name(module):
            return module.DetectGames().name_modul

        sys_path = self.verif_folder(self.__folder_path, self.GAME)
        user_path = self.verif_folder(self.__user_folder_path, self.GAME)
        self.__load(name, plugin_name, self.__plugin_detect, sys_path)
        self.__load(name, plugin_name, self.__plugin_detect, user_path)

    def load_games(self):
        name = 'PluginGames'
        def plugin_name(module):
            return module.PluginGames().name_game

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

    def get_plugin_game_by_name(self, name):
        return self.__plugins_game[name].PluginGames()

    def get_list_plugin_detect_game(self):
        pass

    def get_list_plugin_game(self):
        list_plugin = list()
        for _, plugin in self.__plugins_game.items():
            list_plugin.append(plugin.PluginGames().name_game)

        return list_plugin