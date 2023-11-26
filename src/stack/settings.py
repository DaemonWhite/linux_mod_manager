from gi.repository import Gtk, Adw, GObject

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
        self.window = window

    def enable_windows(self, activate):
        self.prefix_row.set_visible(activate)

    def set_copie_row(self, activate):
        self.copie_row.set_active(activate)

    def set_symbolic_row(self, activate):
        self.symbolic_row.set_active(activate)

    def set_archive_row(self, activate):
         self.archive_row.set_active(activate)