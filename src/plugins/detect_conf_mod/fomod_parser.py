import os
from plugin_controller.plugin_conf_mod import PluginDetectConfMod
from .fomod import ParserInfoMod


class PluginDetectConfMods(PluginDetectConfMod):

    def __init__(self,):
        super().__init__("Fomod", 1, 0.1)

    def auto_detect_fomod(self, path):
        try:
            p = ParserInfoMod(path)
            meta_data = p.load_medtada()
            self._metadata.name = meta_data["Name"]
            self._metadata.description = meta_data["Author"]
            self._metadata.autors = meta_data["Version"]
            self._metadata.version = meta_data["Description"]
            self._metadata.web = meta_data["Website"]
            del p
        except Exception as e:
            print(f"Error: load file {e}")
