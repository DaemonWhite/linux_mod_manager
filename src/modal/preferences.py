from gi.repository import Gtk
from gi.repository import Adw

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/prefference_settings.ui')
class PreferencesLinuxModManager(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesLinuxModManager'

    list_plugin = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__win = window
        self.set_transient_for(self.__win)
        self.plugin = self.__win.plugin
        for plugin in self.__win.list_plugin:
            plug = Adw.SwitchRow.new()
            data_plugin = self.plugin.get_plugin_by_name(plugin)
            plug.set_title(data_plugin.name_game)
            plug.set_subtitle(f"V {data_plugin.plugin_verssion} Authors {data_plugin.authors}")
            plug.set_active(data_plugin.activate)
            self.list_plugin.add(plug)

        print("coucou")