from gi.repository import Gio

from py_mod_manager.const import USER, URI

#TODO Le charger dans window et non dans Current Game

class ApllicationConfiguration(object):
    def __init__(self):
        self.__settings = Gio.Settings(URI)

        # User = 0
        # Plugin = 1
        # Systeme = 2
        self._copy_mode = USER
        self._symb_mode = USER
        self._archive_mode = USER

        self._app_copy = False
        self._app_symb = False
        self._app_archive = False

        self._auto_detect_games = False

        self.load_app_settings()

    def load_app_settings(self):
        self._app_copy = self.__settings.get_boolean("force-default-copy")
        self._app_symb = self.__settings.get_boolean("force-default-symb")
        self._app_archive = self.__settings.get_boolean("force-default-archive")

        self._mode_copy = self.__settings.get_int("mode-default-copy")
        self._mode_symb = self.__settings.get_int("mode-default-symb")
        self._mode_archive = self.__settings.get_int("mode-default-archive")

        self._thread_download = self.__settings.get_int("download-thread")

        self._donwload_base_folder = self.__settings.get_string("donwload-base-folder")
        self._install_base_folder = self.__settings.get_string("install-base-folder")
        self._archive_base_folder = self.__settings.get_string("archive-base-folder")

        self._auto_detect_games = self.__settings.get_boolean("auto-detect-games")

        self._last_game = self.__settings.get_string("last-game-plugin")
        self._last_page = self.__settings.get_string("last-page")

    def save_app_settings(self):
        self.__settings.set_boolean("force-default-copy",self._app_copy)
        self.__settings.set_boolean("force-default-symb",self._app_symb)
        self.__settings.set_boolean("force-default-archive", self._app_archive)

        self.__settings.set_int("mode-default-copy", self._mode_copy)
        self.__settings.set_int("mode-default-symb",self._mode_symb)
        self.__settings.set_int("mode-default-archive",self._mode_archive)

        self.__settings.set_int("download-thread", self._thread_download)

        self.__settings.set_string("donwload-base-folder", self._donwload_base_folder)
        self.__settings.set_string("install-base-folder", self._install_base_folder)
        self.__settings.set_string("archive-base-folder", self._archive_base_folder)

        self.__settings.set_boolean("auto-detect-games",self._auto_detect_games)

        self.__settings.set_string("last-game-plugin", self._last_game)
        self.__settings.set_string("last-page", self._last_page)

    def get_string(self, name: str):
        return self.__settings.get_string(name)

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

    def get_thread_download(self):
        return self._thread_download

    def get_auto_detect_games(self):
        return self._auto_detect_games

    def get_donwload_base_folder(self):
        return self._donwload_base_folder

    def get_install_base_folder(self):
        return self._install_base_folder

    def get_archive_base_folder(self):
        return self._archive_base_folder

    def get_last_game(self):
        return self._last_game

    def get_last_page(self):
        return self._last_page

    def set_string(self, name, data):
        self.__settings.set_string(name, data)

    def set_app_copy(self, copy: bool):
        self._app_copy = copy

    def set_app_archive(self, archive: bool):
        self._app_archive = archive

    def set_app_symb(self, symb: bool):
        self._app_symb = symb

    def set_mode_copy(self, copy: int):
        self._mode_copy = copy

    def set_mode_archive(self, archive: int):
        self._mode_archive = archive

    def set_mode_symb(self, symb: int):
        self._mode_symb = symb

    def set_thread_download(self, nb_thread):
        self._thread_download = nb_thread

    def set_auto_detect_games(self, auto: bool):
        self._auto_detect_games = auto

    def set_donwload_base_folder(self, donwload_base_folder: str):
        self._donwload_base_folder = donwload_base_folder

    def set_install_base_folder(self, install_base_folder: str):
        self._install_base_folder = install_base_folder

    def set_archive_base_folder(self, archive_base_folder: str):
        self._archive_base_folder = archive_base_folder

    def set_last_game(self, last_game: str):
        self._last_game = last_game

    def set_last_page(self, last_page):
        self._last_page = last_page
