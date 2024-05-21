import threading

from dataclasses import dataclass

from mod_handlers.install import InstallSysteme
from mod_handlers.configure import ConfigFile, GenertedModConfig, StateDetect
from utils.files import generate_dict_archive


@dataclass
class InstallTask:
    install_syst: object
    generte_config_mod: object
    config_mod: object
    path_game: str
    path_mod: str
    path_installed: str


class ModManager(object):
    def __init__(self):
        self.__selected = ""
        self.__list_task_mod = {}
        self.__install_fill = []
        self.__config_fill = []
        self.__install_work = False
        self.__config_work = False

        self.__callback_finish_install = self.default_callback
        self.__callback_configuration = self.default_callback

    def init_config(self, mod_plugin) -> bool:
        result = False
        plugin = self.__list_task_mod[mod_plugin]
        print(self.__list_task_mod[mod_plugin])
        try:
            config = generate_dict_archive(False, plugin.path_game)
            conf = plugin.config_mod
            path_installed = plugin.path_installed + "/" + mod_plugin + ".json"
            conf.load(path_installed)
            conf.init_config(config)
            conf.save(path_installed)
            result = True
        except Exception as e:
            print("Error dict traitement : ", e)
            result = False
        return result

    def default_callback(*args):
        print(args)

    def get_install_file(self, file_name, mod_plugin):
        return self.__list_task_mod[mod_plugin].install_syst.get_file(
            file_name
        )

    def set_configuration_callback(self, callback):
        self.__callback_configuration = callback

    def set_callback_finish(self, callback):
        self.__callback_finish_install = callback

    def add_game(self, name: str, path_download: str, path_install: str,
                 path_game: str, path_mod: str, path_installed: str,
                 file_detect: list, folder_detect: list, script_detect: list):
        print("add_game")
        print(path_game)
        print(path_download)
        conf = GenertedModConfig()
        conf.add_list_file_detect(file_detect)
        conf.add_list_folder_detect(folder_detect)
        conf.add_list_script_detect(script_detect)
        conf.set_path_mod(path_mod)

        self.__list_task_mod[name] = InstallTask(
            install_syst=InstallSysteme(path_download, path_install),
            generte_config_mod=conf,
            config_mod=ConfigFile(),
            path_game=path_game,
            path_mod=path_mod,
            path_installed=path_installed,
        )

    def add_install_file(self, file_name, mod_plugin):
        return self.__list_task_mod[mod_plugin].install_syst.append_file(
            file_name
        )

    def select_mod(self, mod_name: str):
        self.__selected = mod_name

    def mod_exist(self, mod_name):
        exist = False
        if self.__list_task_mod.get(mod_name):
            exist = True

        return exist

    def list_installable_mod(self, mod_plugin=""):
        if mod_plugin == "":
            mod_plugin = self.__selected

        return self.__list_task_mod[mod_plugin].install_syst.list_file

    def update_list_install(self, file):
        pass

    def __finish_install(self, mod_plugin, identifiant):
        self.__callback_finish_install(mod_plugin, identifiant)

    def get_first_configuration(self, mod_plugin):
        if len(self.__config_fill) > 0:
            self.__callback_configuration(self.__config_fill[0])

    def end_configuration(self):
        self.__config_fill.pop(0)
        if len(self.__config_fill) > 0:
            self.__callback_configuration(self.__config_fill[0])
        else:
            self.__config_work = False

    def __install(self, mod_plugin, file):
        self.__install_work = True
        mod_plugin = self.__list_task_mod[mod_plugin]
        self.__install_fill.pop(0)

        mod_plugin.generte_config_mod.set_path_mod_analyse(
            mod_plugin.install_syst.path_install + "/" + file.file
        )
        mod_plugin.install_syst.install(file)

        detect_state = mod_plugin.generte_config_mod.auto_detect_config()
        print("detect_state", detect_state)
        if detect_state == StateDetect.HUMAN_INTERVENTION:
            print("ok")
            self.__config_fill.append(
                mod_plugin.generte_config_mod.get_interface_config()
            )
            if not self.__config_work:
                self.__config_work = True
                self.__callback_configuration(self.__config_fill[0])
        else:
            self.__config_fill.append(
                mod_plugin.generte_config_mod.generate_config()
            )
        self.__finish_install(mod_plugin, file)

        if len(self.__install_fill) > 0:
            self.__install_fill[0].start()
        else:
            self.__install_work = False

    def install(self, file, mod_plugin=""):
        if mod_plugin == "":
            mod_plugin = self.__selected

        self.__install_fill.append(
            threading.Thread(
                target=self.__install,
                args=(mod_plugin, file,)
            )
        )

        if not self.__install_work:
            self.__install_fill[0].start()

    def set_config():
        pass

    def set_config_path():
        pass

    def deploy():
        pass

    def conflit():
        pass

    def purge():
        pass
