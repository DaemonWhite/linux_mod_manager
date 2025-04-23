/* window.rs
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

use gtk::prelude::*;
use adw::subclass::prelude::*;
use gtk::{gio, glib};

use crate::config;

use crate::ui::stack::{
    OrderStack,
    SettingsStack,
    ManagementStack
};

mod imp {
    use super::*;

    #[derive(Debug, Default, gtk::CompositeTemplate)]
    #[template(resource = "/fr/daemonwhite/mod_manager/ui/window.ui")]
    pub struct LinuxModManagerWindow {
        // Template widgets
        #[template_child]
        pub main_stack: TemplateChild<adw::ViewStack>,
        #[template_child]
        pub choose_game: TemplateChild<gtk::DropDown>,
        #[template_child]
        pub view_switcher_bar: TemplateChild<adw::ViewSwitcherBar>,
        #[template_child]
        pub order_stack: TemplateChild<OrderStack>,
        #[template_child]
        pub settings_stack: TemplateChild<SettingsStack>,
        #[template_child]
        pub management_stack: TemplateChild<ManagementStack>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for LinuxModManagerWindow {
        const NAME: &'static str = "LinuxModManagerWindow";
        type Type = super::LinuxModManagerWindow;
        type ParentType = adw::ApplicationWindow;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for LinuxModManagerWindow {
        fn constructed(&self) {
            self.parent_constructed();
            let obj = self.obj();
            if config::DEVEL == "devel" {
                obj.add_css_class("devel");
            }

            // self.main_stack.add_titled(
            //     OrderStack::new(application),
            //     "Mod"
            // )

        }
    }
    impl WidgetImpl for LinuxModManagerWindow {}
    impl WindowImpl for LinuxModManagerWindow {}
    impl ApplicationWindowImpl for LinuxModManagerWindow {}
    impl AdwApplicationWindowImpl for LinuxModManagerWindow {}
}

glib::wrapper! {
    pub struct LinuxModManagerWindow(ObjectSubclass<imp::LinuxModManagerWindow>)
        @extends gtk::Widget, gtk::Window, gtk::ApplicationWindow, adw::ApplicationWindow,
        @implements gio::ActionGroup, gio::ActionMap;
}

impl LinuxModManagerWindow {
    pub fn new<P: IsA<gtk::Application>>(application: &P) -> Self {
        glib::Object::builder()
            .property("application", application)
            .build()
    }
}
