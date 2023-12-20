from gi.repository import Gtk, Adw, GObject, GLib, Gio

from mod_handlers.download import DownloadModManager

from py_mod_manager.const import UI_BASE

# TODO Donwload end event change color

class model(GObject.Object, Gio.ListModel):
    __gtype_name__ = 'RowModel'
    def __init(self):
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
    dowbloader_list_box = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        list_mime_type = [
            'application/zip',
            'application/x-rar-compressed',
            'application/x-tar',
            'application/gzip',
            'application/x-7z-compressed'
        ]
        placeholder = Gtk.Label()
        placeholder.set_label("Aucun téléchargement en cours")
        self.dowbloader_list_box.set_placeholder(placeholder)
        self.dowbloader_list_box.set_selection_mode(Gtk.SelectionMode.NONE)

        self.downloader_button.connect("clicked", self.__erase_download_row)

        self.__archive_filter = Gtk.FileFilter()
        self.__archive_filter.set_name("archive")

        self.__download_manager = DownloadModManager()
        self.__download_manager.set_callback_progress(self.__row_update_download)
        self.__download_manager.set_callback_end(self.__event_end_download)

        for mime_type in list_mime_type:
            self.__archive_filter.add_mime_type(mime_type)
        self.import_button.connect("clicked", self.__on_select_files)


    def __erase_download_row(self, button):
        # TODO Ajouter la verification des erreurs
        delete_row = []
        for progress_bar in self.dowbloader_list_box:
            delete_row.append(progress_bar)

        for progress_bar in delete_row:
            self.dowbloader_list_box.remove(progress_bar)

    def __update_subtitle_download(self, progress, total):
        self.downloader_row.set_subtitle(f"{progress}/{total}")
        self.downloader_progress.pulse()
        self.downloader_progress.set_fraction(progress/total)

    def __event_end_download(self, progress, total):
        GLib.idle_add(self.__update_subtitle_download, progress, total)

    def __row_update_download(self, progress, progress_bar):
        def row_update(progress, progress_bar):
            progress_bar.pulse()
            progress_bar.set_fraction(progress)
        GLib.idle_add(row_update, progress, progress_bar[0])

    def __create_downloader_row(self, name, plugin):
        # TODO Create widget
        box = Gtk.Box()
        progress = Gtk.ProgressBar()
        box.append(progress)
        pref = Adw.ActionRow()
        pref.set_title(name)
        pref.set_subtitle(plugin)
        pref.add_suffix(box)
        # self.downloader_row.add_row(pref)
        self.dowbloader_list_box.prepend(pref)
        return progress

    def __on_single_selected(self, dialog, result):
        files = ""
        try:
            # TODO Ajouter la gestion d'erreur flatpak et basic
            files = dialog.open_multiple_finish(result)
            for file in files:
                file_path = file.get_path()
                progress = self.__create_downloader_row(file_path, self.__window.cg.plugin_name)
                self.__download_manager \
                    .append( \
                        file_path, \
                        self.__window.settings.get_donwload_base_folder(),  \
                        self.__window.cg.plugin_name, \
                        progress \
                    )
                self.__event_end_download( \
                    self.__download_manager.total_download_end, \
                    self.__download_manager.total_download, \
                )
        except Exception as e :
            print(e)

    def __on_select_files(self, dialog):
        dialog_for_folder = Gtk.FileDialog()
        dialog_for_folder.set_default_filter(self.__archive_filter)
        dialog_for_folder.set_accept_label("Importer")
        dialog_for_folder.set_title("Importer des mods")
        file = dialog_for_folder.open_multiple(self.__window, None, self.__on_single_selected)


