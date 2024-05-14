from mod_handlers.install import InstallSysteme
import threading


class ModManager(object):
    def __init__(self):
        self.__selected = ""
        self.__list_task_mod = {}
        self.__install_fill = []
        self.__install_work = False

        self.__callback_finish_install = self.default_callback

    def default_callback(*args):
        pass

    def set_default_callback_finish(self, callback):
        self.__callback_finish_install = callback

    def add_mod(self, name, path_download, path_install):
        self.__list_task_mod[name] = {
            'work': False,
            'install_syst': InstallSysteme(path_download, path_install)
        }

    def add_install_file(self, file_name, mod_plugin):
        return self.__list_task_mod[mod_plugin]['install_syst'].append_file(
            file_name
        )

    def select_mod(self, mod_name: str):
        self.__selected = mod_name

    def mod_exist(self, mod_name):
        exist = False
        if self.__list_task_mod.get(mod_name):
            exist = True

        return exist

    def list_no_installed_mod(self, mod_plugin=""):
        if mod_plugin == "":
            mod_plugin = self.__selected

        return self.__list_task_mod[mod_plugin]['install_syst'].no_installed()

    def update_list_install(self, file):
        pass

    def __finish_install(self, mod_plugin, identifiant):
        self.__callback_finish_install(mod_plugin, identifiant)

    def __install(self, mod_plugin, file):
        self.__install_work = True
        self.__list_task_mod[mod_plugin]['install_syst'].install(file)
        self.__install_fill.pop(0)

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
