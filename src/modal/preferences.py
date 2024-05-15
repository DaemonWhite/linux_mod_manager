from gi.repository import Gtk
from gi.repository import Adw

from py_mod_manager.const import *

from utils.current_game import CurrentGame
from utils.plugin_conf import PluginConfig
from utils.xdg import xdg_conf_path

from custom_widget.switch_info_row import SwitchInfoRow


@Gtk.Template(resource_path=UI_BASE+'modal/prefferences.ui')
class PreferencesLinuxModManager(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesLinuxModManager'

    list_games_plugin = Gtk.Template.Child()
    list_auto_detect_games_plugin = Gtk.Template.Child()

    force_copy = Gtk.Template.Child()
    force_symb = Gtk.Template.Child()
    force_archive = Gtk.Template.Child()

    archive_row = Gtk.Template.Child()
    install_row = Gtk.Template.Child()
    download_row = Gtk.Template.Child()

    archive_folder = Gtk.Template.Child()
    install_folder = Gtk.Template.Child()
    download_folder = Gtk.Template.Child()

    preference_copy = Gtk.Template.Child()
    preference_symbolic = Gtk.Template.Child()
    preference_archive = Gtk.Template.Child()

    download_thread = Gtk.Template.Child()

    auto_detect = Gtk.Template.Child()

    expand_default_settings = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.connect("close-request", self.on_destroy)

        self.__win = window
        self.set_transient_for(self.__win)
        self.plugin = self.__win.plugin

        self.preference_copy.connect('notify::selected', self.on_change)
        self.preference_symbolic.connect('notify::selected', self.on_change)
        self.preference_archive.connect('notify::selected', self.on_change)

        self.archive_folder.connect(
            'clicked',
            self.__on_select_folder,
            self.__win.settings.set_archive_base_folder
        )
        self.download_folder.connect(
            'clicked',
            self.__on_select_folder,
            self.__win.settings.set_donwload_base_folder
        )
        self.install_folder.connect(
            'clicked',
            self.__on_select_folder,
            self.__win.settings.set_install_base_folder
        )

        self.__plugin_path = xdg_conf_path()

        self.load_settings()
        self.load_game_plugin()
        self.load_detect_games_plugin()

    def load_settings(self):
        self.force_copy.set_active(self.__win.settings.get_app_copy())
        self.force_symb.set_active(self.__win.settings.get_app_symb())
        self.force_archive.set_active(self.__win.settings.get_app_archive())

        mode_copy = self.__win.settings.get_mode_copy()
        mode_symb = self.__win.settings.get_mode_symb()
        mode_archive = self.__win.settings.get_mode_archive()

        self.download_thread.set_value(
            self.__win.settings.get_thread_download()
        )

        self.preference_copy.set_selected(mode_copy)
        self.preference_symbolic.set_selected(mode_symb)
        self.preference_archive.set_selected(mode_archive)

        path_archive = self.__win.settings.get_archive_base_folder()
        path_download = self.__win.settings.get_donwload_base_folder()
        path_install = self.__win.settings.get_install_base_folder()

        self.archive_row.set_subtitle(path_archive)
        self.download_row.set_subtitle(path_download)
        self.install_row.set_subtitle(path_install)

        if not mode_copy == GLOBAL:
            self.force_copy.set_sensitive(False)
        if not mode_symb == GLOBAL:
            self.force_symb.set_sensitive(False)
        if not mode_archive == GLOBAL:
            self.force_archive.set_sensitive(False)

        self.auto_detect.set_active(
            self.__win.settings.get_auto_detect_games()
        )

    def __create_base_row_plugin(self, plugin):
        plug = SwitchInfoRow()
        plug.set_title(plugin.name)
        plug.set_subtitle(
            f"V {plugin.plugin_version} Authors {plugin.authors}"
        )
        return plug

    def load_detect_games_plugin(self):
        list_plugin = self.__win.list_auto_detect
        for name_plugin, plugin_data in list_plugin.items():
            plugin = plugin_data[0]()
            conf_plugin = plugin_data[1]

            plug = self.__create_base_row_plugin(plugin)

            if plugin.flatpak:
                plug.create_tag("Flatpak")

            if plugin.local:
                plug.create_tag("Local")

            if plugin.windows:
                plug.create_tag("Wine")

            plug.connect(
                "activated",
                self.__active_plugin,
                self.__win.plugin.PLUGIN_DETECT_GAMES
            )
            plug.set_active(conf_plugin.is_enable())
            self.list_auto_detect_games_plugin.add(plug)

    def load_game_plugin(self):
        for name_plugin, plugin_data in self.__win.list_plugin.items():
            plug = SwitchInfoRow()
            plugin = plugin_data[0]()
            plug = self.__create_base_row_plugin(plugin)
            conf_plugin = plugin_data[1]
            for systeme in plugin.systeme:
                plug.create_tag(systeme)
            plug.set_active(conf_plugin.is_enable())
            plug.connect(
                "activated",
                self.__active_plugin,
                self.__win.plugin.PLUGIN_GAMES
            )
            self.list_games_plugin.add(plug)

    def __active_plugin(self, widget, _, plugin_registre):
        print(widget.get_active())
        name_plugin = widget.get_title()
        conf_plugin = self.__win.plugin.get_conf_plugin(
            plugin_registre,
            name_plugin
        )
        conf_plugin.enable(widget.get_active())

    def __on_single_selected(self, dialog, result, callback):
        file = ""
        try:
            # TODO Ajouter la gestion d'erreur flatpak et basic
            file = dialog.select_folder_finish(result).get_path()
            callback(file)
            self.load_settings()
        except Exception as e:
            print(e)

    def __on_select_folder(self, dialog, callback):
        dialog_for_folder = Gtk.FileDialog()
        dialog_for_folder.select_folder(
            self,
            None,
            self.__on_single_selected, callback
        )

    def __verified_change(self, row, value):
        if value == 2:
            row.set_sensitive(True)
        else:
            row.set_sensitive(False)

    def on_change(self, _widget, _):
        mode_copy = self.preference_copy.get_selected()
        mode_symb = self.preference_symbolic.get_selected()
        mode_archive = self.preference_archive.get_selected()

        self.__verified_change(self.force_copy, mode_copy)
        self.__verified_change(self.force_symb, mode_symb)
        self.__verified_change(self.force_archive, mode_archive)

    def save_settings(self):
        # Save Force
        self.__win.settings.set_app_copy(self.force_copy.get_active())
        self.__win.settings.set_app_symb(self.force_symb.get_active())
        self.__win.settings.set_app_archive(self.force_archive.get_active())
        # Save Mode
        self.__win.settings.set_mode_copy(self.preference_copy.get_selected())
        self.__win.settings.set_mode_symb(
            self.preference_symbolic.get_selected()
        )
        self.__win.settings.set_mode_archive(
            self.preference_archive.get_selected()
        )

        self.__win.settings.set_auto_detect_games(
            self.auto_detect.get_active()
        )

        self.__win.settings.set_thread_download(
            self.download_thread.get_value()
        )

        self.__win.settings.save_app_settings()

    def on_destroy(self, _):
        self.save_settings()
        self.__win.reload()
