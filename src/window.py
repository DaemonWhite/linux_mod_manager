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

from gi.repository import Adw
from gi.repository import Gtk

from plugin_controller.plugin import PluginManager

from modal.choose_games import PyModManagerWindowChooseGames

from stack.settings import SettingsStack
from stack.order import OrderStack
from stack.mod import ModStack

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/window.ui')
class PyModManagerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PyModManagerWindow'

    label = Gtk.Template.Child()
    main_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs.get("application")

        self.choose_games = PyModManagerWindowChooseGames(self)

        self.plugin = PluginManager()
        self.plugin.load("/home/matheo/Projets/Python/py_mod_manager/src/plugins")
        self.plugin.get_names_plugin()

        self.show()
        self.page_settings = SettingsStack(self)
        self.page_order = OrderStack(self)
        self.page_mod = ModStack(self)

        self.main_stack.add_titled(
        	child=self.page_mod,
        	name="page_mod",
        	title="Mods"
        )
        self.main_stack.add_titled(
        	child=self.page_order,
        	name="page_order",
        	title="Order"
        )
        self.main_stack.add_titled(
        	child=self.page_settings,
        	name="page_settings",
        	title="Settings"
        )
        self.main_stack.set_visible_child_name("page_mod")
        self.choose_games.show()

