from plugin_controller.plugin_game import PluginGame


class PluginGames(PluginGame):
    def __init__(self):
        super().__init__("Skyrim", "The Elder Scrolls V: Skyrim", 1, 0.1)
        self._nexus_mod = True
        self._systeme = ["win"]
        self.symbolic = False
        self._path_mod = "data"
        self._mode_extention = [".esp", ".esl", ".esm"]
        self.append_recurent_directory("data", "/")
