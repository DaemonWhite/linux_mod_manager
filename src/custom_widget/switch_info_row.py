from gi.repository import Adw, Gtk, Gio, GLib, GObject

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/widget_switch_info_row.ui')
class SwitchInfoRow(Adw.PreferencesRow):
    __gtype_name__ = "SwitchInfoRow"
    __gobject_init__ = "SwitchInfoRow"

    __gproperties__ = {
        'active': ( \
            Gtk.Widget, \
            'Activatable Switch', \
            'The switch to activate when the row is activated.', \
            GObject.ParamFlags.READWRITE \
        ),
    }
    contents = Gtk.Template.Child()

    labels_box = Gtk.Template.Child()
    info_box = Gtk.Template.Child()

    title_label = Gtk.Template.Child()
    subtitle_label = Gtk.Template.Child()

    active_switch = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        b = GObject.BindingGroup.new()
        b.bind("action-name", self.active_switch, "action-name", GObject.BindingFlags.SYNC_CREATE)
        b.bind("action-target", self.active_switch, "action-target", GObject.BindingFlags.SYNC_CREATE)

        self.active_switch.connect("notify::active", self.slider_notify_active_cb )

        simple_action = Gio.SimpleAction(name="activated")
        row_group = Gio.SimpleActionGroup()
        self.active_switch.insert_action_group("row", row_group)
        self.insert_action_group("row", row_group)
        simple_action.connect(
            "activate",
            self.__inverse_switch,
        )
        row_group.add_action(simple_action)

    def parent_e(self, a, b):
        print('coucou')

    def slider_notify_active_cb(self, widget, param):
        print("coucou")
        Gtk.Accessible.update_state(
            self, [Gtk.AccessibleState.CHECKED], [int(self.active_switch.get_active())]
        )
        self.notify("active")

    def __inverse_switch(self, widget, _):
        state = not self.active_switch.get_active()
        self.active_switch.set_active(state)

    def get_title(self):
        return self.title_label.get_label()

    def get_subtitle(self):
        return self.subtitle_label.get_label()

    def get_active(self):
        return self.active_switch.get_active()

    def set_title(self, title):
        self.title_label.set_label(title)

    def set_subtitle(self, subtitle):
        self.subtitle_label.set_label(subtitle)

    def set_active(self, active):
        self.active_switch.set_active(active)

    def create_tag(self, name: str, color):
        #TODO Activer l'ajout de tag avec couleur
        label = Gtk.Label()
        label.set_label(name)
