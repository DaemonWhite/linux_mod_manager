from gi.repository import Adw, Gtk

from custom_widget.check_row import CheckRow
from py_mod_manager.const import UI_BASE
from utils.list_model import ListMultipleSelectModel


@Gtk.Template(resource_path=UI_BASE+'widgets/preference_group_model.ui')
class PreferenceGroupModel(Adw.PreferencesGroup):

    __gtype_name__ = "PreferenceGroupModel"

    listbox_box = Gtk.Template.Child()

    def __init__(self, group, **kwargs):
        super().__init__(**kwargs)
        self.__callback_mouse = self.__default_callback_mouse

        self.list_box = Gtk.ListBox()
        self.list_box.add_css_class("content")
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox_box.prepend(self.list_box)
        self.__model = ListMultipleSelectModel(group.options)
        self.list_box.bind_model(self.__model, self.create_row)
        self.set_title(group.name)

    def __default_callback_mouse(self, roww, description, ilustration, teste):
        print("mouse selected")

    def call_callback(self, roww, description, ilustration, teste):
        self.__callback_mouse(roww, description, ilustration, teste)

    def set_callback(self, callback: callable):
        self.__callback_mouse = callback
        print("power")

    def create_row(self, group_gobject):
        group = group_gobject.object
        print(group)
        check = CheckRow()
        check.set_sensitive(group.activate)
        check.set_title(group.name)
        check.set_subtitle(group.description)
        check.set_enable(group.enable)
        check.connect(
            "focus-mouse",
            self.call_callback,
            group.description,
            group.ilustration
        )
        check.connect_button("toggled", self.selecte_event, group.name)
        return check

    def selecte_event(self, button, name):
        self.__model.enable(name, button.get_active())
