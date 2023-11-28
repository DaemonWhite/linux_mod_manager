from gi.repository import Gtk, Adw, GObject

from py_mod_manager.const import USER, NOTIFY_ACTIVE

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/settings.ui')
class SettingsStack(Adw.Bin):
    __gtype_name__ = 'SettingsStack'

    symbolic_row = Gtk.Template.Child()
    copie_row = Gtk.Template.Child()
    prefix_row = Gtk.Template.Child()
    path_row = Gtk.Template.Child()
    archive_row = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.symbolic_row.connect(NOTIFY_ACTIVE, self.__switch_change, "symbolic")
        self.copie_row.connect(NOTIFY_ACTIVE, self.__switch_change, "copy")
        self.archive_row.connect(NOTIFY_ACTIVE, self.__switch_change, "archive")

    def __switch_change(self, widget, _, data):
        mode = USER
        if data == "symbolic":
            mode = self.__window.cg.get_mode_symb()
        elif data == "copy":
            mode = self.__window.cg.get_mode_copy()
        elif data == "archive":
            mode = self.__window.cg.get_mode_archive()

        if mode == USER:
            self.__window.cg.set_configuration(data, widget.get_active())
            self.__window.cg.save_plugin()

    def enable_windows(self, activate):
        self.prefix_row.set_visible(activate)

    def set_copie_row(self, activate):
        self.copie_row.set_active(activate)

    def set_symbolic_row(self, activate):
        self.symbolic_row.set_active(activate)

    def set_archive_row(self, activate):
         self.archive_row.set_active(activate)