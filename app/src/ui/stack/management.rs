/* management.rs
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
    #[template(resource = "/fr/daemonwhite/mod_manager/ui/stack/management.ui")]
    pub struct ManagementStack {
        #[template_child]
        pub import_button: TemplateChild<gtk::Button>,
        #[template_child]
        pub downloader_row: TemplateChild<adw::ExpanderRow>,
        #[template_child]
        pub downloader_progress: TemplateChild<gtk::ProgressBar>,
        #[template_child]
        pub downloader_button: TemplateChild<gtk::Button>,
        #[template_child]
        pub downloader_list_box: TemplateChild<gtk::ListBox>,
        #[template_child]
        pub deploy_button: TemplateChild<gtk::Button>,
        #[template_child]
        pub purger_button: TemplateChild<gtk::Button>,
        #[template_child]
        pub choose_config: TemplateChild<gtk::DropDown>,
        #[template_child]
        pub install_row: TemplateChild<adw::ExpanderRow>,
        #[template_child]
        pub install_list_row: TemplateChild<gtk::ListBox>,
        #[template_child]
        pub uninstall_row: TemplateChild<adw::ExpanderRow>,
        #[template_child]
        pub uninstall_list_row: TemplateChild<gtk::ListBox>,


    }

    #[glib::object_subclass]
    impl ObjectSubclass for ManagementStack {
        const NAME: &'static str = "ManagementStack";
        type Type = super::ManagementStack;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for ManagementStack {
        fn constructed(&self) {
            let _obj = self.obj();
            self.parent_constructed();
        }
    }

    impl WidgetImpl for ManagementStack {}
    impl BinImpl for ManagementStack {}
}


glib::wrapper! {
    pub struct ManagementStack(ObjectSubclass<imp::ManagementStack>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget;
}

impl ManagementStack {
    pub fn new() -> Self {
        glib::Object::new()
    }
}
