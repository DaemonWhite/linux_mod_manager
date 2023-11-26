from gi.repository import Gtk, Adw, GObject

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/settings.ui')
class SettingsStack(Adw.Bin):
	__gtype_name__ = 'SettingsStack'

	def __init__(self, window, **kwargs):
		super().__init__(**kwargs)
		self.window = window


