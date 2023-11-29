from plugin_controller.plugin_base import PluginBase

class PluginGame(PluginBase):

    def __init__(self, short_name, true_name, version, plugin_version):
        super().__init__(short_name, version, plugin_version)
        self._list_name = [short_name, true_name]
        self._true_name = true_name
        self._systeme = ["linux"]
        self._symbolic = True
        self._archive = True
        self._copie = True
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
        return self._symbolic

    @property
    def archive(self):
        return self._archive

    @property
    def copie(self):
        return self._copie

    @property
    def nexus_mod(self):
        return self._nexus_mod

    @property
    def platform(self):
        return self._platform

    @symbolic.setter
    def symbolic(self, activate):
        self._symbolic = activate