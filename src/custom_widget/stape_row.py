from gi.repository import Adw, Gtk, GObject

from py_mod_manager.const import UI_BASE
from utils.stape import Stape


@Gtk.Template(resource_path=UI_BASE+'widgets/stape_row.ui')
class StapeRow(Adw.ActionRow, Stape):
    __gtype_name__ = "StapeRow"
    __gobject_init__ = "StapeRow"

    __gproperties__ = {
        'active': (
            Gtk.Widget,
            'Activatable Switch',
            'The switch to activate when the row is activated.',
            GObject.ParamFlags.READWRITE
        ),
    }

    box_color = Gtk.Template.Child()

    label_info = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Stape.__init__(self, self.box_color)
