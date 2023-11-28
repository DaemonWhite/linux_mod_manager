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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

from plugin_controller.plugin import PluginManager
from plugin_controller.plugin_game import PluginGame
from plugin_controller.factory import Game

from modal.preferences import PreferencesLinuxModManager
from modal.choose_games import PyModManagerWindowChooseGames

from utils.current_game import CurrentGame
from utils.plugin_conf import PluginConfig
from utils.xdg import xdg_conf_path

from stack.settings import SettingsStack
from stack.order import OrderStack
from stack.mod import ModStack
from stack.error import ErrorStack

from py_mod_manager.const import USER, NOTIFY_SELECT_ITEM, BUILD_TYPE, URI, PKGDATADIR

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/window.ui')
class PyModManagerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PyModManagerWindow'

    main_stack = Gtk.Template.Child()
    choose_game = Gtk.Template.Child()

    view_switcher_title = Gtk.Template.Child()
    view_switcher_bar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs.get("application")

        plugin_path = os.path.join(PKGDATADIR, 'plugins')

        settings = Gio.Settings(URI)
        self.__last_game = settings.get_string('last-game-plugin')
        self.__last_page = settings.get_string('last-page')

        self.choose_games = PyModManagerWindowChooseGames(self)

        if BUILD_TYPE == "devel":
            self.add_css_class(BUILD_TYPE)

        self.app.create_action('preferences', self.__show_prefrences)

        # Start Plugin
        self._plugin = PluginManager(plugin_path, xdg_conf_path())
        self._plugin.load_games()
        self._plugin.load_detect_plugin()
        self.cg = CurrentGame(self._plugin.get_first_plugin_game())

        # Create list plugin
        self._list = Gio.ListStore.new(Game)
        self._list_plugin_game_load = list()

        # Event List plugin
        self._list_plugin = self._plugin.get_list_plugin_game()

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind)
        self.choose_game.set_factory(factory)
        self.__len_enable_support_game = 0

        self.load_support_game()

        # Apply list
        self.choose_game.set_model(self._list)
        self.choose_game.connect(NOTIFY_SELECT_ITEM, self._on_selected_item_notify)

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

        self.select_game(self.search_game_plugin(self.__last_game))

        if self.verif_load_game():
            self.enable_current_plugin()
        # self.show()
        # self.choose_games.show()

    def __change_page(self, widget, _):
         self.__last_page = widget.get_visible_child_name()

    def verif_load_game(self):
        if self.__len_enable_support_game == 0:
            self.main_stack.set_visible_child_name("page_error")
            self.page_error.error_label.set_label("Veulier activer au moins un pluging de jeux")
            self.view_switcher_bar.set_visible(False)
            self.view_switcher_title.set_visible(False)
            return False
        else:
            self.view_switcher_bar.set_visible(True)
            self.view_switcher_title.set_visible(True)
            self.main_stack.set_visible_child_name(self.__last_page)
            return True


    def unload_support_game(self):
        self._list_plugin_game_load = list()
        self.__len_enable_support_game = 0
        self._list.remove_all()

    def load_support_game(self):
        # Add Plugin
        self._list_plugin_game_load = list()
        self.__len_enable_support_game = 0
        for plugin in self._list_plugin:
            conf_plugin = CurrentGame(self._plugin.get_plugin_game_by_name(plugin))
            if conf_plugin.is_enable():
                self._list_plugin_game_load.append(plugin)
                self._list.append(Game(plugin))
                self.__len_enable_support_game += 1

    def search_game_plugin(self, name):
        index = -1
        i=0
        for plugin_name in self._list_plugin_game_load:
            if plugin_name == name:
                index = i
                break
            i+=1
        return index


    def select_game(self, index):
        if index > -1:
            self.choose_game.set_selected(index)

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
        self.verif_sensitive_settings( \
            self.page_settings.symbolic_row, \
            self.cg.get_mode_symb() \
        )

        self.verif_sensitive_settings( \
            self.page_settings.copie_row, \
            self.cg.get_mode_copy() \
        )

        self.verif_sensitive_settings( \
            self.page_settings.archive_row, \
            self.cg.get_mode_archive() \
        )

        self.page_settings.set_symbolic_row(self.cg.symbolic)
        self.page_settings.set_copie_row(self.cg.copy)
        self.page_settings.set_archive_row(self.cg.archive)

        if self.cg.systeme == "win":
            self.page_settings.enable_windows(True)
        else:
            self.page_settings.enable_windows(False)

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
            self.cg.set_current_game( \
                self._plugin.get_plugin_game_by_name(game.game_name) \
            )
        self.enable_current_plugin()

    def on_destroy(self, _):
        if not self.__len_enable_support_game == 0:
            settings = Gio.Settings(URI)
            settings.set_string("last-game-plugin", self.__last_game)
            settings.set_string("last-page", self.__last_page)
