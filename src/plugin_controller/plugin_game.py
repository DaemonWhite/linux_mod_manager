from plugin_controller.plugin_base import PluginBase

# TODO Trouver pk il est charger beaucou de foix au démarage

# TODO Ne sauvegarde pas le système de configuration correctement Probablement un problème d'ordre

class PluginGame(PluginBase):

    def __init__(self, short_name, true_name, version, plugin_version):
        super().__init__(short_name, version, plugin_version, 'games')
        self._list_name = [short_name, true_name]
        self._true_name = true_name
        self._systeme = ["linux"]
        self._add_conf("symbolic", True)
        self._add_conf("archive", True)
        self._add_conf("copy", True)
        self._add_conf("path", "")
        self._add_conf("prefix", "")
        self._add_protected_conf("symbolic")
        self._add_protected_conf("archive")
        self._add_protected_conf("copy")
        self._add_ban_conf("path")
        self._add_ban_conf("prefix")
        self._nexus_mod = False
        self._platform = ["Manual"]

    @property
    def true_name(self):
        return self._true_name

    @property
    def list_name(self):
        return self._list_name

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

    @symbolic.setter
    def symbolic(self, activate: bool):
        self.set_conf("symbolic", activate)

    @archive.setter
    def archive(self, activate: bool):
        self.set_conf("archive", activate)

    @copy.setter
    def copy(self, activate: bool):
        self.set_conf("copy", activate)
