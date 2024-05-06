from plugin_controller.plugin_game import PluginGame

class PluginGames(PluginGame):
    def __init__(self):
        super().__init__("Fallout: New Vegas", "Fallout: New Vegas", 1, 0.1)
        self._nexus_mod = True
        self._systeme = ["win"]
        self.symbolic = False
