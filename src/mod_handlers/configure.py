import os
import json

from dataclasses import dataclass


class ConfigFile():
    def __init__(self):
        self.__configuration = {'main': {}, 'mod': {}}

    def load(self, path) -> bool:
        file = False
        if os.path.isfile(path):
            with open(path, "w") as json_file:
                json.load(self.__configuration, json_file)
            file = True
        return file

    def unload(self):
        self.__configuration = {'main': {}, 'mod': {}}

    def save(self, path):
        print(path)
        with open(path, "w") as json_file:
            json.dump(self.__configuration, json_file)

    def verif_config(self, path):
        pass

    def init_config(self, config):
        self.__configuration['main'] = config

    def add_mod_config(self, mod, config):
        self.__configuration['mod'][mod] = config

    def remove_mod_config(self, mod, config):
        self.__configuration['mod'][mod] = config


@dataclass
class StateDetect:
    NO_DETECT = 0
    DETECTED = 1
    HUMAN_INTERVENTION = 2


class GenertedModConfig():
    def __init__(self):
        self.__path_game = ""
        self.__mod_path = ""
        self.__file_detect = []
        self.__folder_detect = []
        self.__script_detect = []

        self.__config = {}

    def set_path_game(self, path: str):
        self.__path_game = path

    def clear(self):
        self.__file_detect.clear()
        self.__folder_detect.clear()
        self.__script_detect = []

    def append_file_detect(self, file):
        self.__file_detect.append(file)

    def append_folder_detect(self, folder):
        self.__folder_detect.append(folder)

    def append_script_detect(self, script):
        self.__script_detect.append(script)

    def detecte_file(self, path):
        pass

    def detecte_folder(self, path):
        pass

    def detcte_game(self, path):
        pass

    def auto_detect_config(self) -> int:
        is_detected = StateDetect.NO_DETECT
        # for self.__script_detect in self.__script_detect:
        #     return self.__script_detect(self.__path_game)

        for file_and_folder in os.listdir(self.__path_game):
            if os.path.isdir(os.path.join(self.__path_game, file_and_folder)):
                self.detecte_folder(file_and_folder)
            else:
                self.detecte_file(file_and_folder)

        return is_detected
