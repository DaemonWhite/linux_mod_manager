from gi.repository import Gio

class ApllicationConfiguration(object):
    def __init__(self):
        self.__settings = Gio.Settings("fr.daemonwhite.mod_manager")

        # User = 0
        # Plugin = 1
        # Systeme = 2
        self._copy_mode = 0
        self._symb_mode = 0
        self._archive_mode = 0

        self._app_copy = False
        self._app_symb = False
        self._app_archive = False

        self._auto_detect_games = False

        self.load_app_settings()

        self.plugin_games = {}

    def load_app_settings(self):
        self._app_copy = self.__settings.get_boolean("force-default-copy")
        self._app_symb = self.__settings.get_boolean("force-default-symb")
        self._app_archive = self.__settings.get_boolean("force-default-archive")

        self._mode_copy = self.__settings.get_int("mode-default-copy")
        self._mode_symb = self.__settings.get_int("mode-default-symb")
        self._mode_archive = self.__settings.get_int("mode-default-archive")

        self._auto_detect_games = self.__settings.get_boolean("auto-detect-games")

    def save_app_settings(self):
        self.__settings.set_boolean("force-default-copy",self._app_copy)
        self.__settings.set_boolean("force-default-symb",self._app_symb)
        self.__settings.set_boolean("force-default-archive", self._app_archive)

        self.__settings.set_int("mode-default-copy", self._mode_copy)
        self.__settings.set_int("mode-default-symb",self._mode_symb)
        self.__settings.set_int("mode-default-archive",self._mode_archive)

        self.__settings.set_boolean("auto-detect-games",self._auto_detect_games)

    def get_app_copy(self):
        return self._app_copy

    def get_app_archive(self):
        return self._app_archive

    def get_app_symb(self):
        return self._app_symb

    def get_mode_copy(self):
        return self._mode_copy

    def get_mode_archive(self):
        return self._mode_archive

    def get_mode_symb(self):
        return self._mode_symb

    def get_auto_detect_games(self):
        return self._auto_detect_games

    def set_app_copy(self, copy):
        self._app_copy = copy

    def set_app_archive(self, archive):
        self._app_archive = archive

    def set_app_symb(self, symb):
        self._app_symb = symb

    def set_mode_copy(self, copy):
        self._mode_copy = copy

    def set_mode_archive(self, archive):
        self._mode_archive = archive

    def set_mode_symb(self, symb):
        self._mode_symb = symb

    def set_auto_detect_games(self, auto):
        self._auto_detect_games = auto