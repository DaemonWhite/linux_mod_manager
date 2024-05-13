from gi.repository import Adw, Gtk, GObject

from py_mod_manager.const import UI_BASE
from utils.stape import Stape


@Gtk.Template(resource_path=UI_BASE+'widgets/install_row.ui')
class InstallRow(Adw.ActionRow, Stape):
    __gtype_name__ = "InstallRow"
    __gobject_init__ = "InstallRow"

    __gproperties__ = {
        'clicked': (
            Gtk.Widget,
            'Activatable Switch',
            'The switch to activate when the row is activated.',
            GObject.ParamFlags.READWRITE
        ),
    }

    box_color = Gtk.Template.Child()

    install_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Stape.__init__(self, self.box_color)

    def lock(self):
        self.install_button.set_sensitive(False)

    def unlock(self):
        self.install_button.set_sensitive(True)

    def connect(self, callback, *args):
        self.install_button.connect("clicked", callback, self, args)
