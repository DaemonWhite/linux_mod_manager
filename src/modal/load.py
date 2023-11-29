from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/fr/daemonwhite/mod_manager/ui/modal_load.ui')
class PyModManagerWindowModalLoad(Adw.Window):
    __gtype_name__ = 'PyModManagerWindowModalLoad'

    load_stack = Gtk.Template.Child()

    load_status = Gtk.Template.Child()
    result_status = Gtk.Template.Child()
    search_spiner = Gtk.Template.Child()

    close_button = Gtk.Template.Child()

    def __init__(self, windows):
        Adw.Window.__init__(self, title="Choose Games")
        self.__window = windows
        self.set_transient_for(self.__window)
        self.search_spiner.start()

        self.close_button.connect("clicked", self.on_close)

    def do_close_request(self, *_args) -> bool:
        return True

    def on_close(self, _):
        self.destroy()

    def set_name_load(self, name, description):
        title = f'Rechercher de : {name}'
        self.load_status.set_title(title)
        self.load_status.set_description(description)
        self.load_stack.set_visible_child_name("load_status_page")

    def set_name_result(self, result, name, description):
        title = f'{name}'
        self.result_status.set_title(title)
        self.result_status.set_description(description)
        if result:
            self.result_status.set_icon_name('object-select-symbolic')
        else:
            self.result_status.set_icon_name('process-stop-symbolic')
        self.load_stack.set_visible_child_name("result_status_page")
        