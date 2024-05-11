from gi.repository import Adw
from gi.repository import Gtk

from py_mod_manager.const import UI_BASE
from custom_widget.stape_row import StapeRow


@Gtk.Template(resource_path=UI_BASE+'modal/load.ui')
class PyModManagerWindowModalLoad(Adw.Window):
    __gtype_name__ = 'PyModManagerWindowModalLoad'

    load_stack = Gtk.Template.Child()

    stape_configuration = Gtk.Template.Child()

    load_status = Gtk.Template.Child()
    result_status = Gtk.Template.Child()

    close_button = Gtk.Template.Child()

    def __init__(self, windows, name):
        Adw.Window.__init__(self, title="Load")
        self.__window = windows
        self.__stape = 0
        self.__array_stape = []
        self.set_transient_for(self.__window)

        self.stape_configuration.set_title(name)

        self.accept_close = False

        self.close_button.connect("clicked", self.on_close)

    @property
    def nb_stape(self):
        return len(self.__array_stape)

    @property
    def stape(self):
        return self.__stape

    def do_close_request(self, *_args) -> bool:
        if self.accept_close:
            return False
        return True

    def on_close(self, _):
        self.accept_close = True
        self.close()

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

    def add_stape(self, name, description, default_state):
        self.__array_stape.append(StapeRow())
        index = len(self.__array_stape) - 1
        self.__array_stape[index].set_title(name)
        self.__array_stape[index].set_subtitle(description)
        self.stape_configuration.add(self.__array_stape[index])
        return index

    def choose_state(self, index, name):
        self.__array_stape[index].choose_state(name)

    def load_state(self, index, style="work"):
        self.__array_stape[index].start_load_state(style)
