/* error.rs
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
    #[template(resource = "/fr/daemonwhite/mod_manager/ui/stack/error.ui")]
    pub struct ErrorStack {
        #[template_child]
        pub row_enabled: TemplateChild<adw::ExpanderRow>,

        #[template_child]
        pub row_disabled: TemplateChild<adw::ExpanderRow>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for ErrorStack {
        const NAME: &'static str = "ErrorStack";
        type Type = super::ErrorStack;
        type ParentType = adw::Bin;

        fn class_init(klass: &mut Self::Class) {
            klass.bind_template();
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for ErrorStack {
        fn constructed(&self) {
            let _obj = self.obj();
            self.parent_constructed();
        }
    }

    impl WidgetImpl for ErrorStack {}
    impl BinImpl for ErrorStack {}
}


glib::wrapper! {
    pub struct ErrorStack(ObjectSubclass<imp::ErrorStack>)
        @extends gtk::Widget, adw::Bin,
        @implements gtk::Accessible, gtk::Buildable, gtk::ConstraintTarget;
}

impl ErrorStack {
    pub fn new() -> Self {
        glib::Object::new()
    }
}
