from plugin_controller.plugin_base import PluginBase
from mod_handlers.configure import RecurentDataDirectory

# TODO Ne sauvegarde pas le système de configuration correctement Probablement
# un problème d'ordre


class PluginGame(PluginBase):

    def __init__(self, short_name, true_name, version, plugin_version):
        super().__init__(short_name, version, plugin_version, 'games')
        self.__list_name = [short_name, true_name]
        self._true_name = true_name
        self._systeme = ["linux"]
        self.__recurrent_directory = []
        self._mode_extention = []
        self._ignore_extention = []
        self._add_conf("symbolic", True)
        self._add_conf("archive", True)
        self._add_conf("copy", True)
        self._add_conf("path", "")
        self._add_conf("path_download", "")
        self._add_conf("path_install", "")
        self._add_conf("prefix", "")
        self._add_conf("conflit_syst", False)
        self._add_conf("post_conf", False)
        self._add_protected_conf("symbolic")
        self._add_protected_conf("archive")
        self._add_protected_conf("copy")
        self._add_protected_conf("conflit_syst")
        self._add_protected_conf("post_conf")
        self._add_ban_conf("path")
        self._add_ban_conf("path_download")
        self._add_ban_conf("path_install")
        self._add_ban_conf("prefix")
        self._nexus_mod = False
        self._platform = ["Manual"]
        self._same_game_and_mod_folder = True
        self._path_mod = ""

    @property
    def true_name(self):
        return self._true_name

    @property
    def list_name(self):
        return self.__list_name

    @property
    def systeme(self):
        return self._systeme

    @property
    def symbolic(self):
        return self._get_conf('symbolic')

    @property
    def archive(self):
        return self._get_conf('archive')

    @property
    def copy(self):
        return self._get_conf('copy')

    @property
    def nexus_mod(self):
        return self._nexus_mod

    @property
    def platform(self):
        return self._platform

    @property
    def same_game_and_mod_folder(self):
        return self._same_game_and_mod_folder

    @property
    def path_mod(self):
        return self._path_mod

    @property
    def recurrent_directory(self):
        return self.__recurrent_directory

    @property
    def mode_extention(self):
        return self._mode_extention

    @symbolic.setter
    def symbolic(self, activate: bool):
        self.set_conf("symbolic", activate)

    @archive.setter
    def archive(self, activate: bool):
        self.set_conf("archive", activate)

    @copy.setter
    def copy(self, activate: bool):
        self.set_conf("copy", activate)

    def post_traitement(self):
        return True

    def append_name(self, name: str):
        self.__list_name.append(name)

    def append_recurent_directory(self, folder: str, destination: str):
        self.__recurrent_directory.append(
            RecurentDataDirectory(folder, destination)
        )
