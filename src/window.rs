/* window.rs
 *
 * Copyright 2024 Unknown
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

use crate::{config};

mod imp {
    use super::*;

    #[derive(Debug, Default, gtk::CompositeTemplate)]
    #[template(resource = "/fr/daemonwhite/mod_manager/ui/window.ui")]
    pub struct RustLinuxModManagerWindow {
        // Template widgets
        // #[template_child]
        // pub label: TemplateChild<gtk::Label>,
        //
        // pub main_stack: TemplateChild<adw::ViewStack>;
        #[template_child]
        pub main_stack: TemplateChild<adw::ViewStack>,
        #[template_child]
        pub choose_game: TemplateChild<gtk::DropDown>,

        #[template_child]
        pub view_switcher_title: TemplateChild<adw::ViewSwitcher>,

        // #[template_child]
        // pub view: TemplateChild<adw::ViewSwitcher>,
        // #[template_child]
        // pub view_switcher_bar: TemplateChild<adw::ViewSwitcherBar>

    }

    #[glib::object_subclass]
    impl ObjectSubclass for RustLinuxModManagerWindow {
        const NAME: &'static str = "RustLinuxModManagerWindow";
        type Type = super::RustLinuxModManagerWindow;
        type ParentType = adw::ApplicationWindow;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for RustLinuxModManagerWindow {
        fn constructed(&self) {
            self.parent_constructed();

            let obj = self.obj();
            if config::DEVEL != 0 {
                obj.add_css_class("devel");
            }
        }
    }
    impl WidgetImpl for RustLinuxModManagerWindow {}
    impl WindowImpl for RustLinuxModManagerWindow {}
    impl ApplicationWindowImpl for RustLinuxModManagerWindow {}
    impl AdwApplicationWindowImpl for RustLinuxModManagerWindow {}
}

glib::wrapper! {
    pub struct RustLinuxModManagerWindow(ObjectSubclass<imp::RustLinuxModManagerWindow>)
        @extends gtk::Widget, gtk::Window, gtk::ApplicationWindow, adw::ApplicationWindow,        @implements gio::ActionGroup, gio::ActionMap;
}

impl RustLinuxModManagerWindow {
    pub fn new<P: IsA<gtk::Application>>(application: &P) -> Self {
        glib::Object::builder()
            .property("application", application)
            .build()
    }
}

