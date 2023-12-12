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

    def reload(self, name, path , registery_plugin):
        self.unload()
        self.load(name, path, registery_plugin)

    def get_liste_plugins(self):
        return self.__list_plugin.copy()

    def unload(self):
        self.__list_plugin.clear()
