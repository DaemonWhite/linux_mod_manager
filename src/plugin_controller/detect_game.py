class DetectGames(DetectGame):

    def __init__(self,):
        self._game_detected = False
        self._game = str()
        self._path = str()

    def _search_game(self):
        pass

    def search_game(self, game):
        self.game = game
        return self._game_detected, self._path