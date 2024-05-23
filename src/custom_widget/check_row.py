from gi.repository import Adw, Gtk, GObject

from py_mod_manager.const import UI_BASE


@Gtk.Template(resource_path=UI_BASE+'widgets/check_row.ui')
class CheckRow(Adw.ActionRow):
    __gtype_name__ = "CheckRow"
    __gobject_init__ = "CheckRow"

    __gsignals__ = {
        'focus-mouse': (GObject.SignalFlags.RUN_FIRST, None, (object,))
    }

    check_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.focus_controller = Gtk.EventControllerMotion.new()
        self.add_controller(self.focus_controller)

        self.focus_controller.connect("enter", self.do_enter)

    def connect_button(self, notify, callback, name):
        self.check_button.connect(
            notify,
            callback,
            name
        )

    def do_enter(self, controler, a, b):
        self.emit("focus-mouse", self)

    def get_enable(self) -> bool:
        return self.check_button.get_active()

    def set_enable(self, value: bool):
        print(value)
        self.check_button.set_active(value)
