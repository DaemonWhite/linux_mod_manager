import os
import json
class PluginConfig(object):

    def __init__(self):
        self.__existe = False

        self.__plugin = {
            "version" : 0.0,
            "copy" : False,
            "archive" : True,
            "symbolic" : True,
            "path" : "",
            "prefix" : "",
        }


    @property
    def _existe(self):
        return self.__existe

    @property
    def _path(self):
        return self.__path

    def _set_path(self, name, path):
        self.__existe = False
        self.__path =  os.path.join(path, f"{name}.json")
        if os.path.isfile(self.__path):
            self.__existe = True


    def add_configuration(self, data):
        self.__plugin += data

    def set_configuration(self, name,  data):
        self.__plugin[name] = data

    def _load_plugin(self):
        with open(self.__path, "r") as json_file:
            self.__plugin = json.load(json_file)

    def save_plugin(self):
        plugin = {}
        if self.__existe:
            with open(self.__path, "r") as json_file:
                plugin = json.load(json_file)
        if not self.__plugin == plugin:
            with open(self.__path, "w") as json_file:
                json.dump(self.__plugin, json_file)

    def get_plugin_configuration(self, name):
        return self.__plugin[name]


