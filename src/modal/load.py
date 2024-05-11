from gi.repository import Adw
from gi.repository import Gtk

import threading

from py_mod_manager.const import UI_BASE
from custom_widget.stape_row import StapeRow


@Gtk.Template(resource_path=UI_BASE+'modal/load.ui')
class PyModManagerWindowModalLoad(Adw.Window):
    __gtype_name__ = 'PyModManagerWindowModalLoad'

    load_stack = Gtk.Template.Child()

    stape_box = Gtk.Template.Child()

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

    def __default_callback():
        pass

    def set_name_load(self, name, description=""):
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

    def __task_syncrone(self):
        index = -1
        result = False
        for stape in self.__array_stape:
            index += 1
            self.load_status.set_description(
                stape['title_description']
            )
            self.load_state(index)
            result = stape['callback']()
            if result:
                self.choose_state(index, "success")
            else:
                self.choose_state(index, "error")
                if stape["error_end"]:
                    print("End")
                    break

        print(index)
        if result:
            self.set_name_result(
                    result,
                    self.load_status.get_title(),
                    self.__array_stape[index]['success_description']
                )
        else:
            self.set_name_result(
                    result,
                    self.load_status.get_title(),
                    self.__array_stape[index]['error_description']
                )

    def task_synchrone(self):
        thread_task_synchrone = threading.Thread(
            target=self.__task_syncrone
        )
        thread_task_synchrone.start()

    def add_stape(
            self,
            name,
            description="",
            title_description="",
            success_description="",
            error_description="",
            callback=None,
            error_end=False
    ):
        self.stape_box.set_visible(True)

        if not callback:
            callback = self.__default_callback

        self.__array_stape.append({
            'row': StapeRow(),
            'title_description': title_description,
            'success_description': success_description,
            'error_description': error_description,
            'callback': callback,
            'error_end': error_end
        })
        index = len(self.__array_stape) - 1
        self.__array_stape[index]['row'].set_title(name)
        self.__array_stape[index]['row'].set_subtitle(description)
        self.stape_configuration.add(self.__array_stape[index]['row'])
        return index

    def choose_state(self, index, name):
        self.__array_stape[index]['row'].choose_state(name)

    def load_state(self, index, style="work"):
        self.__array_stape[index]['row'].start_load_state(style)
