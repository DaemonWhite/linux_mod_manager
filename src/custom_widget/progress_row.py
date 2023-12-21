from gi.repository import Adw, Gtk, Gio, GLib, GObject

from py_mod_manager.const import UI_BASE

@Gtk.Template(resource_path=UI_BASE+'widgets/progress_row.ui')
class ProgressRow(Adw.ActionRow):
    __gtype_name__ = "ProgressRow"
    __gobject_init__ = "ProgressRow"

    __gproperties__ = {
        'active': ( \
            Gtk.Widget, \
            'Activatable Switch', \
            'The switch to activate when the row is activated.', \
            GObject.ParamFlags.READWRITE \
        ),
    }

    progress_bar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__FINISH = 1
        self.__PROGRESS = 0
        self.__ERROR = 2
        self.__WARNING = 3

        self.__state = 0

    @property
    def state(self):
        return self.__state

    @property
    def FINISH(self):
        return self.__FINISH

    @property
    def PROGRESS(self):
        return self.__PROGRESS

    @property
    def ERROR(self):
        return self.__ERROR

    def set_progress_fraction(self, progress: float):
        self.progress_bar.pulse()
        self.progress_bar.set_fraction(progress)
        self.__PROGRESS = 0

    def progress_style(self, state):
        def remove_css(name):
            if self.progress_bar.has_css_class(name):
                self.progress_bar.remove_css_class(name)

        remove_css("progress_valide")
        remove_css("progress_error")
        remove_css("progress_warning")

        self.__state = state

        if self.__FINISH == state:
            self.progress_bar.add_css_class("progress_valide")
        elif self.__ERROR == state:
            self.progress_bar.add_css_class("progress_error")
        elif self.__WARNING == state:
            self.progress_bar.add_css_class("progress_warning")
        else:
            self.__state = 0
