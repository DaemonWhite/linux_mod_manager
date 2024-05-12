from py_mod_manager.const import VERSION_PLUGIN


class PluginBase(object):

    def __init__(self, name, version, plugin_version, type_plugin):
        self.__plugin_manager_version = VERSION_PLUGIN
        self.__name = name
        self.__plugin_version = plugin_version
        self._authors = "Unknow"

        self.__type_plugin = type_plugin

        self.__list_ban_conf = ["version"]
        self.__list_protected_conf = [str]

        self.__plugin_conf = {
            "version": version
        }

    @property
    def name(self):
        return self.__name

    @property
    def type_plugin(self):
        return self.__type_plugin

    @property
    def version(self):
        return self.__plugin_conf['version']

    @property
    def plugin_version(self):
        return self.__plugin_version

    @property
    def authors(self):
        return self._authors

    def _add_ban_conf(self, name: str):
        self.__list_ban_conf.append(name)

    def _add_protected_conf(self, name: str):
        self.__list_protected_conf.append(name)

    def verif_banned_conf(self, name):
        valide_banned = False
        for banned in self.__list_ban_conf:
            if name == banned:
                valide_banned = True
                print("Keys baned")
                valide_banned
        return valide_banned

    def _add_conf(self, name, value):
        if not self.verif_banned_conf(name):
            self.__plugin_conf[name] = value

    def set_conf(self, name: str, value):
        valide = False
        if self.verif_banned_conf(name):
            valide = True
            print("banned ", name)
            return valide

        for name_conf, _ in self.__plugin_conf.items():
            if name_conf == name:
                if type(self.__plugin_conf[name]) == type(value):
                    valide = True
                    self.__plugin_conf[name] = value
                else:
                    print(f"Kye {name} type no valide,")
                break

        if not valide:
            print(f"Key {name} no exist")
        return valide

    def _get_conf(self, name):
        return self.__plugin_conf[name]

    def get_plugin_conf(self):
        return self.__plugin_conf.copy()
