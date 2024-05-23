from gi.repository import Adw, Gtk, Gio, GObject

from py_mod_manager.const import UI_BASE


@Gtk.Template(resource_path=UI_BASE+'widgets/switch_info_row.ui')
class SwitchInfoRow(Adw.PreferencesRow):
    __gtype_name__ = "SwitchInfoRow"
    __gobject_init__ = "SwitchInfoRow"

    __gsignals__ = {
        'activated': (GObject.SignalFlags.RUN_FIRST, None, (object,)),
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
        b.bind(
            "action-name",
            self.active_switch,
            "action-name",
            GObject.BindingFlags.SYNC_CREATE
        )
        b.bind(
            "action-target",
            self.active_switch,
            "action-target",
            GObject.BindingFlags.SYNC_CREATE
        )

        self.active_switch.connect(
            "notify::active",
            self.slider_notify_active_cb
        )

        self.demo_group = Gio.SimpleActionGroup()
        self.insert_action_group("row", self.demo_group)
        simple_action = Gio.SimpleAction(name="activated")
        simple_action.connect(
            "activate",
            self.__inverse_switch
        )
        self.demo_group.add_action(simple_action)

    def slider_notify_active_cb(self, widget, param):
        Gtk.Accessible.update_state(
            self, [Gtk.AccessibleState.CHECKED],
            [int(self.active_switch.get_active())]
        )
        self.emit("activated", self)

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
        super().set_title(title)
        self.title_label.set_label(title)

    def set_subtitle(self, subtitle):
        self.subtitle_label.set_label(subtitle)

    def set_active(self, active):
        self.active_switch.set_active(active)

    def create_tag(self, name: str, color=""):
        # TODO Activer l'ajout de tag avec couleur
        box = Gtk.Box()
        label = Gtk.Label()
        label.set_label(name)
        box.append(label)
        label.set_margin_top(2)
        label.set_margin_bottom(2)
        label.set_margin_start(5)
        label.set_margin_end(5)
        self.info_box.append(box)
        context = box.get_style_context()
        context_label = label.get_style_context()
        if not color == "":
            context_label.add_class(color)
        context.add_class('card')
        context.add_class('activatable')
