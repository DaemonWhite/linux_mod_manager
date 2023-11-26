import importlib
import os

class PluginManager(object):

	def __init__(self):
		self.__plugins = dict()

	def load(self, folder_path):
		for file_name in os.listdir(folder_path):
			if file_name.endswith(".py") and file_name != "__init__.py":
				print(file_name)
				plugin_name = os.path.splitext(file_name)[0]
				spec = importlib.util.spec_from_file_location("PluginGames", f"{folder_path}/{file_name}")
				print(f"{folder_path}/{file_name}")
				module = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(module)
				# module = importlib.import_module(f"{folder_path}/{file_name}")
				self.__plugins[plugin_name] = module


	def get_names_plugin(self):
		for plugin_name, plugin in self.__plugins.items():
			print(f"Nom du plugin {self.__plugins} et {plugin}")
			az = plugin.PluginGames()
			az.ba()

	def get_list_plugin(self):
		list_plugin = []
		for plugin_name in self.__plugins.items():
			list_plugin.append(plugin_name)

		return list_plugin