import importlib
import os

class PluginManager(object):

    def __init__(self):
        self.__plugins = dict()

    def load(self, folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".py") and file_name != "__init__.py":
                plugin_name = os.path.splitext(file_name)[0]
                spec = importlib.util.spec_from_file_location("PluginGames", f"{folder_path}/{file_name}")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.__plugins[module.PluginGames().name_game] = module

    def get_first_plugin(self):
        plugin = None
        for _, plug in self.__plugins.items():
            plugin = plug
            break
        return  plugin.PluginGames()

    def get_plugin_by_name(self, name):
        return self.__plugins[name].PluginGames()

    def get_list_plugin(self):
        list_plugin = tuple()
        for _, plugin in self.__plugins.items():
            list_plugin += tuple([plugin.PluginGames().name_game])

        return list_plugin