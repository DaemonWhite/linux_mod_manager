from utils.conf import ApllicationConfiguration

class CurrentGame(ApllicationConfiguration):

    def __init__(self, current_game):
        super().__init__()
        self.__current_game = current_game

    def set_current_game(self, current_game):
        self.__current_game = current_game

    def set_copy(self):
        self._default_force