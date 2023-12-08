from gi.repository import Gtk
from gi.repository import Adw

from py_mod_manager.const import *

from utils.current_game import CurrentGame
from utils.plugin_conf import PluginConfig
from utils.xdg import xdg_conf_path

from custom_widget.switch_info_row import SwitchInfoRow


@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/prefference_settings.ui')
class PreferencesLinuxModManager(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesLinuxModManager'

    list_games_plugin = Gtk.Template.Child()
    list_auto_detect_games_plugin = Gtk.Template.Child()

    force_copy = Gtk.Template.Child()
    force_symb = Gtk.Template.Child()
    force_archive = Gtk.Template.Child()

    preference_copy = Gtk.Template.Child()
    preference_symbolic = Gtk.Template.Child()
    preference_archive = Gtk.Template.Child()

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

        self.__plugin_path = xdg_conf_path()

        self.load_settings()
        self.load_game_plugin()
        self.load_detect_games_plugin()

    def load_settings(self):
        self.force_copy.set_active(self.__win.cg.get_app_copy())
        self.force_symb.set_active(self.__win.cg.get_app_symb())
        self.force_archive.set_active(self.__win.cg.get_app_archive())

        mode_copy = self.__win.cg.get_mode_copy()
        mode_symb = self.__win.cg.get_mode_symb()
        mode_archive = self.__win.cg.get_mode_archive()

        self.preference_copy.set_selected(mode_copy)
        self.preference_symbolic.set_selected(mode_symb)
        self.preference_archive.set_selected(mode_archive)

        if not mode_copy == GLOBAL:
            self.force_copy.set_sensitive(False)
        if not mode_symb == GLOBAL:
            self.force_symb.set_sensitive(False)
        if not mode_archive == GLOBAL:
            self.force_archive.set_sensitive(False)

        self.auto_detect.set_active(self.__win.cg.get_auto_detect_games())

    def __create_base_row_plugin(self, plugin):
        plug = SwitchInfoRow()
        plug.set_title(plugin.name)
        plug.set_subtitle(f"V {plugin.plugin_version} Authors {plugin.authors}")
        return plug

    def load_detect_games_plugin(self):
        list_plugin = self.__win.plugin.get_list_plugin_detect_game()
        for name_plugin in list_plugin:
            plugin = self.plugin.get_plugin_detect_game_by_name(name_plugin)
            conf_plugin = PluginConfig(plugin)
            conf_plugin.set_path_plugin(plugin.name, self.__plugin_path)
            if not conf_plugin.existe:
                conf_plugin.save_plugin()

            conf_plugin.load_plugin()
            plug = self.__create_base_row_plugin(plugin)
            plug.connect(NOTIFY_ACTIVE, self.__active_detect_game_plugin)
            plug.set_active(conf_plugin.is_enable())
            self.list_auto_detect_games_plugin.add(plug)

    def load_game_plugin(self):
        for name_plugin in self.__win.list_plugin:
            plug = SwitchInfoRow()
            plugin = self.plugin.get_plugin_game_by_name(name_plugin)
            plug = self.__create_base_row_plugin(plugin)
            conf_plugin = CurrentGame(plugin)
            plug.set_active(conf_plugin.is_enable())
            plug.connect(NOTIFY_ACTIVE, self.__active_game_plugin)
            self.list_games_plugin.add(plug)

    def __active_game_plugin(self, widget, _):
        name_plugin = widget.get_title()
        plugin = self.plugin.get_plugin_game_by_name(name_plugin)
        conf_plugin = CurrentGame(plugin)
        conf_plugin.enable(widget.get_active())

    def __active_detect_game_plugin(self, widget, _):
        name_plugin = widget.get_title()
        plugin = self.plugin.get_plugin_detect_game_by_name(name_plugin)
        conf_plugin = PluginConfig(plugin)
        conf_plugin.set_path_plugin(plugin.name, self.__plugin_path)
        if not conf_plugin.existe:
            conf_plugin.save_plugin()
        conf_plugin.load_plugin()
        conf_plugin.enable(widget.get_active())

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
        self.__win.cg.set_app_copy(self.force_copy.get_active())
        self.__win.cg.set_app_symb(self.force_symb.get_active())
        self.__win.cg.set_app_archive(self.force_archive.get_active())
        # Save Mode
        self.__win.cg.set_mode_copy(self.preference_copy.get_selected())
        self.__win.cg.set_mode_symb(self.preference_symbolic.get_selected())
        self.__win.cg.set_mode_archive(self.preference_archive.get_selected())

        self.__win.cg.set_auto_detect_games(self.auto_detect.get_active())

        self.__win.cg.save_app_settings()

    def on_destroy(self, _):
        self.save_settings()
        self.__win.reload()

