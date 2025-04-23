/* settinfs.rs
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
use gtk::{glib, CompositeTemplate};

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/fr/daemonwhite/mod_manager/ui/stack/settings.ui")]
    pub struct SettingsStack {
    #[template_child]
    pub information_group: TemplateChild<adw::PreferencesGroup>,
    #[template_child]
    pub symbolic_row: TemplateChild<adw::SwitchRow>,
    #[template_child]
    pub copie_row: TemplateChild<adw::SwitchRow>,
    #[template_child]
    pub prefix_row: TemplateChild<adw::ActionRow>,
    #[template_child]
    pub prefix_folder: TemplateChild<gtk::Button>,
    #[template_child]
    pub path_row: TemplateChild<adw::ActionRow>,
    #[template_child]
    pub archive_row: TemplateChild<adw::SwitchRow>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for SettingsStack {
        const NAME: &'static str = "SettingsStack";
        type Type = super::SettingsStack;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for SettingsStack {
        fn constructed(&self) {
            let _obj = self.obj();
            self.parent_constructed();
        }
    }

    impl WidgetImpl for SettingsStack {}
    impl BinImpl for SettingsStack {}
}


glib::wrapper! {
    pub struct SettingsStack(ObjectSubclass<imp::SettingsStack>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget;
}

impl SettingsStack {
    pub fn new() -> Self {
        glib::Object::new()
    }
}
