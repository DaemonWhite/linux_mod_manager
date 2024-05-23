from gi.repository import Gtk, Gio, Gdk

from py_mod_manager.const import UI_BASE


# TODO Ajouter des dots animer
@Gtk.Template(resource_path=UI_BASE+'widgets/preference_mod_stackpage.ui')
class PreferenceModStackPage(Gtk.Box):

    __gtype_name__ = "PreferenceModStackPage"

    picture = Gtk.Template.Child()
    label = Gtk.Template.Child()
    groups_box = Gtk.Template.Child()

    def __init__(self, **kwarks):
        super().__init__(**kwarks)

    def change_description(self, roww, description, ilustration, teste):
        print(teste)
        self.label.set_label(ilustration)
        file = Gio.File.new_for_path(teste)
        self.picture.set_file(file)

    def add_group_box(self, group):
        group.set_callback(self.change_description)
        self.groups_box.prepend(group)
