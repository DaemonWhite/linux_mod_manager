# window.py
#
# Copyright 2023 Unknown
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import threading
import time

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk

from plugin_controller.factory import Game

from modal.preferences import PreferencesLinuxModManager
from modal.choose_games import PyModManagerWindowChooseGames
from modal.load import PyModManagerWindowModalLoad

from mod_handlers.mod import ModManager

from utils.current_game import CurrentGame
from utils.conf import ApllicationConfiguration
# from utils.files import generate_dict_archive, lower_case_recursif
from utils.plugin_loaders import PluginManager
from utils.create_default_mod_path import create_default_mod_path

from stack.settings import SettingsStack
from stack.order import OrderStack
from stack.mod import ModStack
from stack.error import ErrorStack

from py_mod_manager.const import (
    USER, NOTIFY_SELECT_ITEM, BUILD_TYPE, UI_BASE, URL
)


@Gtk.Template(resource_path=UI_BASE+'window.ui')
class PyModManagerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PyModManagerWindow'

    main_stack = Gtk.Template.Child()
    choose_game = Gtk.Template.Child()

    view_switcher_title = Gtk.Template.Child()
    view_switcher_bar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs.get("application")
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource(URL+'/css/style.css')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # TODO Plugins additional loader
        # plugin_path = os.path.join(PKGDATADIR, 'plugins')

        self.settings = ApllicationConfiguration()
        create_default_mod_path(self.settings)

        self.__started = False

        self.__last_game = self.settings.get_last_game()
        self.__last_page = self.settings.get_last_page()

        self.choose_games = PyModManagerWindowChooseGames(self)

        if BUILD_TYPE == "devel":
            self.add_css_class(BUILD_TYPE)

        self.app.create_action('preferences', self.__show_prefrences)

        # Start Plugin
        self._plugin = PluginManager()
        self.cg = CurrentGame(self.settings)
        self.mod_manager = ModManager()

        # Create list plugin game
        self._list = Gio.ListStore.new(Game)
        self._list_plugin_game_load = list()

        # Create list plugin auto_detect_game
        self._list_auto_detect = self._plugin.get_list_plugin(
            self._plugin.PLUGIN_DETECT_GAMES
        )

        # Event List plugin
        self._list_plugin = self._plugin.get_list_plugin(
            self._plugin.PLUGIN_GAMES
        )

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind)
        self.choose_game.set_factory(factory)
        self.__len_enable_support_game = 0

        self.load_support_game()

        # Apply list
        self.choose_game.set_model(self._list)
        self.choose_game.connect(
            NOTIFY_SELECT_ITEM,
            self._on_selected_item_notify
        )

        self.page_settings = SettingsStack(self)
        self.page_order = OrderStack(self)
        self.page_mod = ModStack(self)
        self.page_error = ErrorStack(self)

        self.main_stack.add_titled(
            child=self.page_order,
            name="page_order",
            title="Order"
        ).set_icon_name("view-list-symbolic")
        self.main_stack.add_titled(
            child=self.page_mod,
            name="page_mod",
            title="Mods"
        ).set_icon_name("application-x-addon-symbolic")
        self.main_stack.add_titled(
            child=self.page_settings,
            name="page_settings",
            title="Settings"
        ).set_icon_name("preferences-other-symbolic")

        self.main_stack.add_named(
            child=self.page_error,
            name="page_error"
        )
        self.connect("close-request", self.on_destroy)

        self.main_stack.set_visible_child_name(self.__last_page)
        self.main_stack.connect("notify::visible-child", self.__change_page)

    def on_start(self):
        self.select_game(self.search_game_plugin(self.__last_game))
        if self.verif_load_game():
            self.enable_current_plugin()

        self.__started = True

    def configure_game(self):
        result = self.cg.auto_detect_path_game(
            self._plugin,
            self._list_auto_detect
        )

        if result:
            self.cg.plugin_conf = True
            self.enable_current_plugin()

        return result

    def auto_detect_game(self):
        load_modal = PyModManagerWindowModalLoad(
            self,
            "Etape de configuration du jeu"
        )
        load_modal.set_name_load(self.cg.name)
        load_modal.add_stape(
            name="Cherche le jeux",
            title_description="Veullier patienter pendant que le système \
cherche votre jeux",
            error_description="N'a pas étais trouver",
            callback=self.configure_game,
            error_end=True
        )
        load_modal.add_stape(
            name="Application du post traitement",
            title_description="Veullier patienter pendant que le système \
applique le poste traitement",
            callback=self.cg.post_traitement
        )
        load_modal.add_stape(
            name="Creation de l'intégritée",
            title_description="Le jeu à étais correctement configurer",
            callback=self.cg.init_conflit_syst
        )
        load_modal.show()
        load_modal.task_synchrone()

    def __change_page(self, widget, _):
        PAGE = widget.get_visible_child_name()
        if PAGE == "page_order" or PAGE == "page_mod" or PAGE == "page_settings":
            self.__last_page = widget.get_visible_child_name()

    def verif_load_game(self):
        if self.__len_enable_support_game == 0:
            self.main_stack.set_visible_child_name("page_error")
            self.page_error.error_label.set_label(
                "Veulier activer au moins un pluging de jeux"
            )
            self.view_switcher_bar.set_visible(False)
            self.view_switcher_title.set_visible(False)
            return False
        else:
            self.view_switcher_bar.set_visible(True)
            self.view_switcher_title.set_visible(True)
            self.main_stack.set_visible_child_name(self.__last_page)
            return True

    def reload(self):
        self.__started = False
        self.unload_support_game()
        self.load_support_game()
        self.select_game(self.search_game_plugin(self.__last_game))
        if self.verif_load_game():
            self.enable_current_plugin()
        self.__started = True

    def unload_support_game(self):
        self._list_plugin_game_load = list()
        self.__len_enable_support_game = 0
        self._list.remove_all()

    def load_support_game(self):
        # Add Plugin
        self._list_plugin_game_load = list()
        self.__len_enable_support_game = 0
        for plugin_name, plugin_data in self._list_plugin.items():
            if plugin_data[1].is_enable():
                self._list_plugin_game_load.append(plugin_name)
                self._list.append(Game(plugin_name))
                self.__len_enable_support_game += 1

    def search_game_plugin(self, name: str) -> int:
        index = -1
        i = 0
        for plugin_name in self._list_plugin_game_load:
            if plugin_name == name:
                index = i
                break
            i += 1
        return index

    def select_game(self, index: int):
        if self.__len_enable_support_game == 0:
            print('Not selected games')
            return False

        game = self.choose_game.get_selected_item().game_name
        if index > -1:
            game = self._list_plugin_game_load[index]
            self.choose_game.set_selected(index)

        self.cg.set_current_game(
            self._plugin.get_plugin(self._plugin.PLUGIN_GAMES, game),
            self._plugin.get_conf_plugin(self._plugin.PLUGIN_GAMES, game)
        )

    @property
    def list_auto_detect(self):
        return self._list_auto_detect

    @property
    def list_plugin(self):
        return self._list_plugin

    @property
    def plugin(self):
        return self._plugin

    def verif_sensitive_settings(self, row, value):
        if value == USER:
            row.set_sensitive(True)
        else:
            row.set_sensitive(False)

    def enable_current_plugin(self):
        if not self.cg.plugin_conf and self.settings.get_auto_detect_games():
            self.auto_detect_game()

        if self.cg.path_download == "":
            self.cg.path_download = self.settings.get_donwload_base_folder()

        if self.cg.path_install == "":
            self.cg.path_install = self.settings.get_install_base_folder()

        self.cg.generated_default_path()
        if not self.mod_manager.mod_exist(self.cg.plugin_name):
            self.mod_manager.add_mod(
                self.cg.plugin_name,
                os.path.join(
                    self.cg.path_download,
                    self.cg.plugin_name,
                ),
                os.path.join(
                    self.cg.path_install,
                    self.cg.plugin_name,
                ),
            )
        self.mod_manager.select_mod(self.cg.plugin_name)
        self.page_mod.reload_mod()

        self.verif_sensitive_settings(
            self.page_settings.symbolic_row,
            self.settings.get_mode_symb()
        )

        self.verif_sensitive_settings(
            self.page_settings.copie_row,
            self.settings.get_mode_copy()
        )

        self.verif_sensitive_settings(
            self.page_settings.archive_row,
            self.settings.get_mode_archive()
        )

        self.page_settings.set_symbolic_row(self.cg.symbolic)
        self.page_settings.set_copie_row(self.cg.copy)
        self.page_settings.set_archive_row(self.cg.archive)

        self.page_settings.set_path_row(self.cg.path_game)
        self.page_settings.set_prefix_row(self.cg.path_prefix)

        path_error = False
        if self.cg.path_game == "":
            path_error = True

        if self.cg.systeme == ["win"]:
            self.page_settings.enable_windows(True)
            if self.cg.path_prefix == "":
                path_error = True
        else:
            self.page_settings.enable_windows(False)

        if path_error:
            self.page_settings.path_state("error")
        else:
            self.page_settings.path_state("success")

        if self.cg.conflit_syst or self.cg.post_conf:
            self.page_settings.post_traitement_state("success")
        else:
            self.page_settings.post_traitement_state("error")

    def __show_prefrences(self, _, _1):
        pref = PreferencesLinuxModManager(self)
        pref.present()

    def _on_factory_setup(self, factory, list_item):
        label = Gtk.Label()
        list_item.set_child(label)

    def _on_factory_bind(self, factory, list_item):
        label = list_item.get_child()
        game = list_item.get_item()
        label.set_text(game.game_name)

    def _on_selected_item_notify(self, dropdown, _):
        if not self.__len_enable_support_game == 0:
            game = dropdown.get_selected_item()
            self.__last_game = game.game_name
            self.cg.set_current_game(
                self._plugin.get_plugin(
                    self._plugin.PLUGIN_GAMES,
                    game.game_name
                ),
                self._plugin.get_conf_plugin(
                    self._plugin.PLUGIN_GAMES,
                    game.game_name
                )
            )
        if self.__started:
            self.enable_current_plugin()

    def on_destroy(self, _):
        if not self.__len_enable_support_game == 0:
            self.settings.set_last_game(self.__last_game)
            self.settings.set_last_page(self.__last_page)
            self.settings.save_app_settings()
