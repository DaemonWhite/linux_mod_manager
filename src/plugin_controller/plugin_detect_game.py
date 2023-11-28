from plugin_controller.plugin_base import PluginBase

class PluginDetectGame(PluginBase):

    def __init__(self, name, version, plugin_version):
        super().__init__(name, version, plugin_version)
        self._game_detected = False
        self._game = str()
        self._path = str()

    def _search_game(self):
        pass

    def search_game(self, game):
        self.game = game
        return self._game_detected, self._path