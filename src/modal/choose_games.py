from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/modal_choose_games.ui')
class PyModManagerWindowChooseGames(Adw.Window):
	__gtype_name__ = 'PyModManagerWindowChooseGames'

	def __init__(self, windows):
		Adw.Window.__init__(self, title="Choose Games")
		self.__window = windows
		self.set_transient_for(self.__window)