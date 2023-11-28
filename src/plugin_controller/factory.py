from gi.repository import GObject

class Game(GObject.Object):
    __gtype_name__ = 'Country'

    def __init__(self, game_name):
        super().__init__()

        self._game_name = game_name

    @GObject.Property
    def game_name(self):
        return self._game_name