from gi.repository import Gtk
from gi.repository import Adw
from gi.repository import Gio

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/prefference_settings.ui')
class PreferencesLinuxModManager(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesLinuxModManager'

    list_games_plugin = Gtk.Template.Child()

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
        self.__settings = Gio.Settings("fr.daemonwhite.mod_manager")

        self.__win = window
        self.set_transient_for(self.__win)
        self.plugin = self.__win.plugin

        self.load_settings()

        for plugin in self.__win.list_plugin:
            plug = Adw.SwitchRow.new()
            data_plugin = self.plugin.get_plugin_by_name(plugin)
            plug.set_title(data_plugin.name_game)
            plug.set_subtitle(f"V {data_plugin.plugin_verssion} Authors {data_plugin.authors}")
            plug.set_active(data_plugin.activate)
            self.list_games_plugin.add(plug)

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

        if not mode_copy == 2:
            self.force_copy.set_sensitive(False)
        if not mode_symb == 2:
            self.force_symb.set_sensitive(False)
        if not mode_archive == 2:
            self.force_archive.set_sensitive(False)

        self.auto_detect.set_active(self.__settings.get_boolean("auto-detect-games"))

    def save_settings(self):
        pass