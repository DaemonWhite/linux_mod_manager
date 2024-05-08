import os

import utils

from gi.repository import Gtk, Adw, GObject, GLib, Gio

from dialout.replace import DialoutReplace

from mod_handlers.download import DownloadModManager, verif_download_exist_file

from custom_widget.progress_row import ProgressRow
from py_mod_manager.const import UI_BASE

from utils.files import slice_path_in_file

# TODO Donwload end event change color

class model(GObject.Object, Gio.ListModel):
    __gtype_name__ = 'RowModel'
    def __init__(self):
        super.__init__()

@Gtk.Template(resource_path=UI_BASE+'stack/mod.ui')
class ModStack(Adw.Bin):
    __gtype_name__ = 'ModStack'

    import_button = Gtk.Template.Child()

    install_row = Gtk.Template.Child()
    configure_row = Gtk.Template.Child()
    download_row = Gtk.Template.Child()

    downloader_row = Gtk.Template.Child()
    downloader_progress = Gtk.Template.Child()
    downloader_button = Gtk.Template.Child()
    downloader_list_box = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__kwargs = kwargs
        self.__window = window
        list_mime_type = [
            'application/zip',
            'application/x-rar-compressed',
            'application/x-tar',
            'application/gzip',
            'application/x-7z-compressed'
        ]

        self.__array_file_exist = []
        self.__exist_fill_popup = False

        placeholder = Gtk.Label()
        placeholder.set_label("Aucun téléchargement en cours")
        self.downloader_list_box.set_placeholder(placeholder)
        self.downloader_list_box.set_selection_mode(Gtk.SelectionMode.NONE)

        self.downloader_button.connect("clicked", self.__erase_download_row)

        self.__archive_filter = Gtk.FileFilter()
        self.__archive_filter.set_name("archive")

        self.__download_manager = DownloadModManager(
            self.__window.settings.get_thread_download()
        )
        self.__download_manager.set_callback_progress(
            self.__row_update_download
        )
        self.__download_manager.set_callback_end(self.__event_end_download)

        for mime_type in list_mime_type:
            self.__archive_filter.add_mime_type(mime_type)
        self.import_button.connect("clicked", self.__on_select_files)

    def __event_array_file_exist_choose(self, dialog, choose):
        if dialog.choose_finish(choose) == "y":
            self.__download_append(
                self.__array_file_exist[0][0],
                self.__array_file_exist[0][1]
            )

        self.__array_file_exist.pop(0)
        self.__exist_fill_popup = False
        self.__launch_dialout_exist_fill()

    def __erase_download_row(self, button):
        # TODO Ajouter la verification des erreurs
        delete_row = []
        for progress_row in self.downloader_list_box:
            if type(progress_row) == type(ProgressRow()) and not progress_row.PROGRESS == progress_row.state :
                delete_row.append(progress_row)

        self.__download_manager.clear()

        self.__event_end_download(
            self.__download_manager.total_download_end,
            self.__download_manager.total_download,
        )

        for progress_row in delete_row:
            self.downloader_list_box.remove(progress_row)

    def __update_subtitle_download(self, progress, total):
        self.downloader_row.set_subtitle(f"{progress}/{total}")
        self.downloader_progress.pulse()
        if total == 0:
            self.downloader_progress.set_fraction(0)
        else:
            self.downloader_progress.set_fraction(progress/total)

    def __event_end_download(
        self,
        progress,
        total,
        state_copy=False,
        progress_bar=None
    ):
        if state_copy:
            GLib.idle_add(progress_bar.progress_style, progress_bar.FINISH)
            self.__row_update_download(progress, [progress_bar])
        GLib.idle_add(self.__update_subtitle_download, progress, total)

    def __row_update_download(self, progress, progress_bar):
        def row_update(progress, progress_bar):
            progress_bar.set_progress_fraction(progress)
        GLib.idle_add(row_update, progress, progress_bar[0])

    def __create_downloader_row(self, name, plugin):
        # TODO Create widget
        progress = ProgressRow()
        progress.set_title(name)
        progress.set_subtitle(plugin)
        self.downloader_list_box.prepend(progress)
        return progress

    def __on_single_selected(self, dialog, result):
        files = ""
        try:
            print(self.__window.cg.plugin_name)
            # TODO Ajouter la gestion d'erreur flatpak et basic
            files = dialog.open_multiple_finish(result)
            for file in files:
                file_path = file.get_path()
                if not verif_download_exist_file(
                    file_path,
                    os.path.join(
                        self.__window.settings.get_donwload_base_folder(),
                        self.__window.cg.plugin_name
                    )
                ):
                    self.__download_append(
                        file_path,
                        self.__window.cg.plugin_name
                    )
                else:
                    self.__donwload_append_exist_fill(
                        file_path,
                        self.__window.cg.plugin_name
                    )
        except Exception as e:
            print(e)

        self.__launch_dialout_exist_fill()

    def __on_select_files(self, dialog):
        dialog_for_folder = Gtk.FileDialog()
        dialog_for_folder.set_default_filter(self.__archive_filter)
        dialog_for_folder.set_accept_label("Importer")
        dialog_for_folder.set_title("Importer des mods")
        dialog_for_folder.open_multiple(
            self.__window,
            None,
            self.__on_single_selected
        )

    def __launch_dialout_exist_fill(self):
        print("dialout")
        if len(self.__array_file_exist) > 0:
            self.__exist_fill_popup = True
            dialout_replace = DialoutReplace(self.__window)
            dialout_replace.set_replace(
                self.__array_file_exist[0][1],
                slice_path_in_file(self.__array_file_exist[0][0])
            )
            dialout_replace.choose(
                callback=self.__event_array_file_exist_choose
            )
            dialout_replace.present()

    def __donwload_append_exist_fill(self, file_path, plugin):
        self.__array_file_exist.append((file_path, plugin))

    def __download_append(self, file_path, plugin):
        progress = self.__create_downloader_row(file_path, plugin)

        self.__download_manager.append(
            file_path,
            self.__window.settings.get_donwload_base_folder(),
            plugin,
            progress
        )
        self.__event_end_download(
            self.__download_manager.total_download_end,
            self.__download_manager.total_download,
        )
