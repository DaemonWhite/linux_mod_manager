from plugin_controller.detect_game import DetectGame

class DetectGames(DetectGame):

    def __init__(self,):
        super.__init__()

    def _search_game(self):
        pass

    def search_game(self, game):
        self.game = game
        return self._game_detected, self._path