from gi.repository import Gtk, Adw, GObject

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/error.ui')
class ErrorStack(Adw.Bin):
    __gtype_name__ = 'ErrorStack'

    error_label = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window


