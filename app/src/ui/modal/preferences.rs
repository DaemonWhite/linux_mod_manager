/* preferences.rs
 *
 * Copyright 2025 DaemonWhite
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

use adw::subclass::prelude::*;
use gtk::{glib, CompositeTemplate, gio};


mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/fr/daemonwhite/mod_manager/ui/modal/preferences.ui")]
    pub struct PreferencesLinuxModManager {
    }

    #[glib::object_subclass]
    impl ObjectSubclass for PreferencesLinuxModManager {
        const NAME: &'static str = "PreferencesLinuxModManager";
        type Type = super::PreferencesLinuxModManager;
        type ParentType = adw::PreferencesDialog;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
            // klass.bind_template_callbacks();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for PreferencesLinuxModManager {
        fn constructed(&self) {
            let _obj = self.obj();
            self.parent_constructed();
        }
    }

    impl WidgetImpl for PreferencesLinuxModManager {}
    impl AdwDialogImpl for PreferencesLinuxModManager {}
    impl PreferencesDialogImpl for PreferencesLinuxModManager {}
}


glib::wrapper! {
    pub struct PreferencesLinuxModManager(ObjectSubclass<imp::PreferencesLinuxModManager>)
        @extends gtk::Widget, adw::Dialog, adw::PreferencesDialog,
        @implements gio::ActionGroup, gio::ActionMap, gtk::Accessible, gtk::Buildable,
                    gtk::ConstraintTarget, gtk::Native, gtk::Root, gtk::ShortcutManager;
}

impl PreferencesLinuxModManager {
}

impl Default for PreferencesLinuxModManager {
    fn default() -> Self {
        glib::Object::new()
    }
}
