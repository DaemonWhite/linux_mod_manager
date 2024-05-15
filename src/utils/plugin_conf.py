import os
import json

from utils.xdg import xdg_conf_path


# TODO Re-protéger set_path
class PluginConfig(object):

    def __init__(self, plugin):
        self.__existe = False

        self.__base_path = ['plugin_conf', plugin.type_plugin]
        self.__path = ""
        self.__plugin = {
            "enable": True,
            "plugin_conf": False,
        }
        for name, data in plugin.get_plugin_conf().items():
            self.__plugin[name] = data

    def __repr__(self):
        return f"PluginConfig(path: {self.__path},\
\nbase_path:{self.__base_path},plugin:\n{self.__plugin})"

    @property
    def conflit_syst(self):
        return bool(self.__plugin["conflit_syst"])

    @property
    def post_conf(self):
        return bool(self.__plugin["post_conf"])

    @property
    def existe(self):
        return self.__existe

    @property
    def path_plugin(self):
        return self.__path

    def set_path_plugin(self, name, base_path):
        self.__existe = False

        for path in self.__base_path:
            base_path = os.path.join(base_path, path)
            if not os.path.isdir(base_path):
                os.makedirs(base_path)

        self.__path = os.path.join(base_path, f"{name}.json")
        if os.path.isfile(self.__path):
            self.__existe = True

    def enable_init_conflit_syst(self, enable):
        self.__plugin["conflit_syst"] = enable
        self.save_plugin()

    def enable_post_conf(self, enable):
        self.__plugin["post_conf"] = enable
        self.save_plugin()

    def enable(self, enable):
        self.__plugin["enable"] = enable
        self.save_plugin()

    def is_enable(self):
        return bool(self.__plugin["enable"])

    def add_configuration(self, data):
        self.__plugin += data

    def set_configuration(self, name,  data):
        self.__plugin[name] = data

    def load_plugin(self):
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
