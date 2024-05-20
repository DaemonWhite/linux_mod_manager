import os
import json

from utils.files import generate_dict_archive
from dataclasses import dataclass


@dataclass
class RecurentDataDirectory:
    folder: str
    destination: str


@dataclass
class ChoiceType:
    SELECT_ONE: int = 0
    SELECT_MULTIPLE: int = 0


@dataclass
class ChoiceOptions:
    name: str
    destination: str
    mod_path: str


@dataclass
class StateDetect:
    NO_DETECT = 0
    DETECTED = 1
    HUMAN_INTERVENTION = 2


class ConfigInterface():
    def __init__(self):
        self.__page = {}
        self.__index = 0

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if len(self.__page) < self.__index:
            return self.__page.keys()[self.__index]
        else:
            raise StopIteration

    def __repr__(self):
        data_text = "Page Empty"
        for page in self.__page:
            data_text = f"page -> {self.__page[page]}\n"

        return data_text

    def add_page(self, name):
        self.__page[name] = {}

    def add_select(
        self, page: str, group: str, select_type: ChoiceType,
        options: list = []
    ):

        self.__page[page][group] = {
            "type": select_type,
            "options": options
        }

    def add_options(self, page: str, group: str, option: ChoiceOptions):
        self.__page[page][group]["options"].append(option)

    def get_pages(self):
        self.__page

    def generate_config(self):
        pass


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
        with open(path, "w") as json_file:
            json.dump(self.__configuration, json_file)

    def init_config(self, config):
        self.__configuration['main'] = config

    def add_mod_config(self, mod, config):
        self.__configuration['mod'][mod] = config

    def remove_mod_config(self, mod, config):
        self.__configuration['mod'][mod] = config


class GenertedModConfig():
    def __init__(self):
        self.__path_game = ""
        self.__mod_path = ""

        self.__file_detect = []
        self.__folder_detect = []
        self.__script_detect = []

        self.__file_detected = []
        self.__folder_detected = []

        self.__simple_config = {
            "metadata": {"name": "", "version": ""},
            "path": [], "conflit": []
        }
        self.__config = ConfigInterface()

    def set_path_mod_analyse(self, path: str):
        self.__path_game = path

    def set_path_mod(self, path):
        self.__mod_path = path

    def clear(self):
        self.__file_detect.clear()
        self.__folder_detect.clear()
        self.__script_detect = []

    def add_list_file_detect(self, files: list):
        self.__file_detect = files

    def add_list_folder_detect(self, folder: list):
        self.__folder_detect = folder

    def add_list_script_detect(self, script: list):
        self.__script_detect = script

    def detecte_file(self, path, suffix=None):
        dirs = []
        path_suffix = ""
        if suffix:
            path_suffix = os.path.join(path, suffix)
            dirs = os.listdir(path_suffix)
        else:
            path_suffix = path
            dirs = os.listdir(path)
            suffix = ""

        detected = False

        folders = []

        for file in dirs:
            test_file = os.path.join(path_suffix, file)
            if os.path.isfile(test_file):
                print("file: ", file)
                for detect_file in self.__file_detect:
                    if file.endswith(detect_file):
                        self.__file_detected.append(suffix + "/" + file)
                        detected = True
                        break
            elif os.path.isdir(test_file):
                if suffix:
                    folders.append(suffix + "/" + file)
                else:
                    print("file: " + file)
                    folders.append(file)
            if detected:
                break

        for folder in folders:
            self.detecte_file(path, folder)

    def detecte_folder(self, path):
        pass

    def detcte_game(self, path):
        pass

    def auto_detect_config(self) -> int:
        is_detected = StateDetect.NO_DETECT
        # for self.__script_detect in self.__script_detect:
        #     return self.__script_detect(self.__path_game)

        self.detecte_file(self.__path_game)
        print(len(self.__file_detect))
        if len(self.__file_detect) > 1:
            is_detected = StateDetect.HUMAN_INTERVENTION
            print("coucou")
            self.__config.add_page("Mods")
            self.__config.add_select(
                "Mods",
                "Selectioner les mods",
                ChoiceType.SELECT_MULTIPLE
            )
            for relative_path in self.__file_detected:
                self.__config.add_options(
                    "Mods",
                    "Selectioner les mods",
                    ChoiceOptions(
                        name=relative_path,
                        destination=relative_path,
                        mod_path=self.__mod_path + "/" + relative_path
                    )
                )

        return is_detected

    def get_interface_config(self):
        return self.__config

    def generate_config(self):
        for path_config in self.__file_detected:
            self.__simple_config['path'].append(path_config)
            self.__simple_config['conflit'] = generate_dict_archive(
                os.path.join(self.__path_game, path_config)
            )

        return self.__simple_config
