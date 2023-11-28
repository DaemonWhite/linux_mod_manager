from plugin_controller.plugin_game import PluginGame

class PluginGames(PluginGame):
    def __init__(self):
        super().__init__("Oblivion", 1, 0.1)
        self._nexus_mod = True

    def ba(self):
        print("ba")