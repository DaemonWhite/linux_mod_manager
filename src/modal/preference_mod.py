from gi.repository import Adw, Gtk

from py_mod_manager.const import UI_BASE
from custom_widget.check_row import CheckRow
from custom_widget.preference_mod_stackpage import PreferenceModStackPage
from custom_widget.preference_group_model import PreferenceGroupModel
from utils.list_model import ListMultipleSelectModel


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

        self.next_button.connect("clicked", self.__next)
        self.previous_button.connect("clicked", self.__previous)

        self.__stack_pages = []

        self.__count_page = 0
        self.__index_page = 0

    def add_page(self, widget, name):
        self.stack.add_child(widget).set_name(name)
        self.__stack_pages.append(name)

        self.__rename_position()

    def __rename_position(self):
        length = len(self.__stack_pages) - 1

        if self.__index_page == 0:
            self.previous_button.set_label("Anuler")
        else:
            self.previous_button.set_label("Précédent")

        if length >= 0 and self.__index_page < length:
            self.next_button.set_label("Suivant")
        else:
            self.next_button.set_label("Valider")

    def __next(self, _):
        if self.__index_page >= len(self.__stack_pages) - 1:
            self.destroy()
        else:
            self.__index_page += 1
            self.stack.set_visible_child_full(
                self.__stack_pages[self.__index_page],
                Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
            )
            self.__rename_position()

    def __previous(self, _):
        if self.__index_page <= 0:
            self.destroy()
        else:
            self.__index_page -= 1
            self.stack.set_visible_child_full(
                self.__stack_pages[self.__index_page],
                Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
            )
            self.__rename_position()

    def create_row(teste, group_gobject):
        group = group_gobject.object
        check = CheckRow()
        check.set_sensitive(group.activate)
        check.set_title(group.name)
        check.set_subtitle(group.description)
        return check

    def set_page_conf(self, conf):
        print(conf)
        for page in conf:
            page_stack = PreferenceModStackPage()
            for group in page.groups:
                pref_group = PreferenceGroupModel(group)
                page_stack.add_group_box(pref_group)

            self.add_page(page_stack, page.name)

    def callback(self, callback):
        pass
