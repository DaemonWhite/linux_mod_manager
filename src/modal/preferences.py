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
        self.connect("close-request", self.on_destroy)

        self.__win = window
        self.set_transient_for(self.__win)
        self.plugin = self.__win.plugin

        self.preference_copy.connect('notify::selected', self.on_change)
        self.preference_symbolic.connect('notify::selected', self.on_change)
        self.preference_archive.connect('notify::selected', self.on_change)

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

        self.auto_detect.set_active(self.__win.cg.get_auto_detect_games())

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