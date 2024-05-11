from gi.repository import Adw, Gtk, Gio, GLib, GObject

from py_mod_manager.const import UI_BASE


class State(object):

    def __init__(self, icon, style):
        self.__icon = icon
        self.__style = style

    @property
    def icon(self):
        return self.__icon

    @property
    def style(self):
        return self.__style


@Gtk.Template(resource_path=UI_BASE+'widgets/stape_row.ui')
class StapeRow(Adw.ActionRow):
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

    image_status = Gtk.Template.Child()
    spinner_status = Gtk.Template.Child()
    label_info = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__current_state = "stop"
        self.__state = {
            "error": State("cross-large-circle-filled-symbolic", "error"),
            "success": State("check-round-outline2-symbolic", "success"),
            "stop": State("stop-sign-large-outline-symbolic", "neutral"),
            "warning": State("warning-outline-symbolic", "warning"),
        }

    def get_styles(self):
        self.__state[self.__current_state].get_style()

    def get_state(self):
        self.__state[self.__current_state].get_icon()

    def choose_state(self, name):
        state = self.__state.get(name)
        if state:
            self.spinner_status.stop()
            self.image_status.set_visible(True)
            self.spinner_status.set_visible(False)

            self.__current_state = name
            self.image_status.set_from_icon_name(
                state.icon
            )
            self.box_color.set_css_classes(["state-icon", state.style])

    def add_state(self, name, icone, styles):
        pass

    def start_load_state(self, styles="neutral"):
        self.box_color.set_css_classes(["state-icon", styles])
        self.image_status.set_visible(False)
        self.spinner_status.set_visible(True)
        self.spinner_status.start()
