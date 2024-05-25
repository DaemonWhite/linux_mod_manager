from plugin_controller.plugin_base import PluginBase
from mod_handlers.configure import ConfigInterface, MetaData


class PluginDetectConfMod(PluginBase):

    def __init__(self, name, version, plugin_version):
        super().__init__(name, version, plugin_version, "DetectConfMod")
        self._config = ConfigInterface()
        self._metadata = MetaData(
            name="", description="", autors="", version="", web=""
        )

    def get_metafata(self):
        return self._metadata

    def get_interface_configuration(self):
        return self._config

    def auto_detect_fomod(self, path):
        pass
