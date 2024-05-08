from gi.repository import Gtk, Adw

from py_mod_manager.const import UI_BASE

class DialoutReplace(Adw.MessageDialog):
    def __init__(self, window):
        super().__init__()
        self.__window = window
        self.set_transient_for(self.__window)
        self.add_response("n", "Non")
        self.add_response("y", "Oui")
        self.set_response_appearance("n", Adw.ResponseAppearance.DESTRUCTIVE)
        self.set_response_appearance("y", Adw.ResponseAppearance.SUGGESTED)

    def set_replace(self, heading, body):
        self.set_heading(f"Voulez-vous remplacer le mod dans {heading}")
        self.set_body(f"Il y'a un déjà un fichier au nom de {body} voulez vous le remplacer ? ")
