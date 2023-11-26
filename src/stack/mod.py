from gi.repository import Gtk, Adw, GObject

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/mod.ui')
class ModStack(Adw.Bin):
    __gtype_name__ = 'ModStack'

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window


