from gi.repository import Adw
from gi.repository import Gtk

from py_mod_manager.const import UI_BASE

@Gtk.Template(resource_path=UI_BASE+'modal/choose_games.ui')
class PyModManagerWindowChooseGames(Adw.Window):
	__gtype_name__ = 'PyModManagerWindowChooseGames'

	def __init__(self, windows):
		Adw.Window.__init__(self, title="Choose Games")
		self.__window = windows
		self.set_transient_for(self.__window)
