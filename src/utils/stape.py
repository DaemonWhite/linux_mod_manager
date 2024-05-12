from gi.repository import Adw, Gtk, GObject


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


class Stape(object):

    def __init__(self, box):
        MARGIN = 5
        self.__box = box
        self.__image = Gtk.Image()
        self.__image.set_halign(True)
        self.__image.set_valign(True)
        self.__image.set_margin_start(MARGIN)
        self.__image.set_margin_end(MARGIN)
        self.__image.set_margin_top(MARGIN)
        self.__image.set_margin_bottom(MARGIN)
        self.__image.set_icon_size(Gtk.IconSize.LARGE)
        self.__image.set_from_icon_name("stop-sign-large-outline-symbolic")

        self.__spinner = Gtk.Spinner()
        self.__spinner.set_halign(True)
        self.__spinner.set_valign(True)
        self.__spinner.set_margin_start(MARGIN)
        self.__spinner.set_margin_end(MARGIN)
        self.__spinner.set_margin_top(MARGIN)
        self.__spinner.set_margin_bottom(MARGIN)
        self.__spinner.set_visible(False)

        self.__box.prepend(self.__image)
        self.__box.prepend(self.__spinner)

        self.__box.set_css_classes(["large-icons"])

        self.__current_state = "stop"
        self.__state = {
            "error": State("cross-large-circle-filled-symbolic", "error"),
            "success": State("check-round-outline2-symbolic", "success"),
            "stop": State("stop-sign-large-outline-symbolic", "neutral"),
            "warning": State("warning-outline-symbolic", "warning"),
        }

    def get_styles(self):
        return self.__state[self.__current_state].get_style()

    def get_state(self):
        self.__state[self.__current_state].get_icon()

    def choose_state(self, name):
        state = self.__state.get(name)
        if state:
            self.__spinner.stop()
            self.__image.set_visible(True)
            self.__spinner.set_visible(False)

            self.__current_state = name
            self.__image.set_from_icon_name(
                state.icon
            )
            self.__box.set_css_classes(["state-icon", state.style])

    def add_state(self, name, icone, styles):
        pass

    def start_load_state(self, styles="neutral"):
        self.__box.set_css_classes(["state-icon", styles])
        self.__image.set_visible(False)
        self.__spinner.set_visible(True)
        self.__spinner.start()
