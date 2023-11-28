from plugin_controller.plugin_detect_game import PluginDetectGame

class PluginDetectGames(PluginDetectGame):

    def __init__(self,):
        super().__init__('Steam', 1, 0.1)

    def _search_game(self):
        pass