from gi.repository import Adw, Gtk, Gio, GLib, GObject

#TODO Ajouter les property ou autre pour que la recherche marche

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

    def create_tag(self, name: str, color=""):
        #TODO Activer l'ajout de tag avec couleur
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
