from gi.repository import Gtk, Adw, GObject

from py_mod_manager.const import UI_BASE

@Gtk.Template(resource_path=UI_BASE+'stack/order.ui')
class OrderStack(Adw.Bin):
    __gtype_name__ = 'OrderStack'

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
