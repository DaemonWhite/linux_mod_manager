from py_mod_manager.const import VERSION_PLUGIN

class PluginBase(object):

    def __init__(self, name, version, plugin_version):
        self.__plugin_manager_version = VERSION_PLUGIN
        self.__name = name
        self.__version = version
        self.__plugin_version = plugin_version
        self._authors = "Unknow"

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    @property
    def plugin_version(self):
        return self.__plugin_version

    @property
    def authors(self):
        return self._authors
