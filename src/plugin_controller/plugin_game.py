class PluginGame(object):

    def __init__(self, name_game, version, plugin_verssion):
        self.__name_game = name_game
        self.__version = version
        self.__plugin_verssion = plugin_verssion
        self._activate = True
        self._authors = "Uknow"
        self._systeme = ["linux"]
        self._symbolic = True
        self._archive = True
        self._copie = True
        self._nexus_mod = False
        self._platform = ["Manual"]

    @property
    def name_game(self):
        return self.__name_game

    @property
    def version(self):
        return self.__version

    @property
    def plugin_verssion(self):
        return self.__plugin_verssion

    @property
    def activate(self):
        return self._activate

    @property
    def authors(self):
        return self._authors

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