from plugin_controller.plugin_game import PluginGame


class PluginGames(PluginGame):
    def __init__(self):
        super().__init__("Oblivion", "The Elder Scrolls IV: Oblivion", 1.0, 0.1)
        self._nexus_mod = True
        self._path_mod = "data"
