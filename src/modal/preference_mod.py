from gi.repository import Adw, Gtk

from py_mod_manager.const import UI_BASE


@Gtk.Template(resource_path=UI_BASE+'modal/preference_mod.ui')
class PyModManagerWindowModalPreferenceMod(Adw.Window):
    __gtype_name__ = 'PyModManagerWindowModalPreferenceMod'

    previous_button = Gtk.Template.Child()
    next_button = Gtk.Template.Child()

    stack = Gtk.Template.Child()

    def __init__(self, window):
        super().__init__()
        self.__window = window
        self.set_transient_for(self.__window)

        self.next_button.connect("clicked", self.__previous)
        self.previous_button.connect("clicked", self.__previous)

        self.__count_page = 0
        self.__index_page = 0

    def __next(self, _):
        self.__count_page -= 1
        if self.__index_page >= self.__count_page:
            self.destroy()

    def __previous(self, _):
        self.__count_page -= 1
        if self.__index_page <= 0:
            self.destroy()

    def set_page_conf(self, conf):
        print(conf)
        for page in conf:
            print(page)

    def callback(self, callback):
        pass
