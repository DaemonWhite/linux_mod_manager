from gi.repository import Gtk, Adw

from py_mod_manager.const import USER, NOTIFY_ACTIVE, UI_BASE
from custom_widget.stape_row import StapeRow


@Gtk.Template(resource_path=UI_BASE+'stack/settings.ui')
class SettingsStack(Adw.Bin):
    __gtype_name__ = 'SettingsStack'

    information_group = Gtk.Template.Child()

    symbolic_row = Gtk.Template.Child()
    copie_row = Gtk.Template.Child()
    archive_row = Gtk.Template.Child()

    prefix_row = Gtk.Template.Child()
    path_row = Gtk.Template.Child()

    game_folder = Gtk.Template.Child()
    prefix_folder = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.symbolic_row.connect(
            NOTIFY_ACTIVE,
            self.__switch_change,
            "symbolic"
        )
        self.copie_row.connect(NOTIFY_ACTIVE, self.__switch_change, "copy")
        self.archive_row.connect(
            NOTIFY_ACTIVE,
            self.__switch_change,
            "archive"
        )

        self.game_folder.connect("clicked", self.__on_select_folder, "path")
        self.prefix_folder.connect(
            "clicked",
            self.__on_select_folder,
            "prefix"
        )
        self.__path_stape_row = StapeRow()
        self.__path_stape_row.set_title("Chemin du jeux et du prefix")
        self.__path_stape_row.set_subtitle(
            "Pour corriger indiquer le chemin du jeu ou/et du prefix.\
\nRéinstaler le jeu peut corriger des problèmes si ça persiste "
        )
        self.__configure_stape_row = StapeRow()
        self.__configure_stape_row.set_title("Configuration du jeu")
        self.__configure_stape_row.set_subtitle(
            "Appuer sur le bouton configurer pour corriger les poblèmes"
        )
        self.information_group.add(self.__path_stape_row)
        self.information_group.add(self.__configure_stape_row)

    def __on_single_selected(self, dialog, result, path):
        file = ""
        try:
            file = dialog.select_folder_finish(result).get_path()
            self.__window.cg.set_configuration(path, file)
            self.__window.cg.save_plugin()
            self.__window.enable_current_plugin()
        except Exception as e:
            print(e)

    def __on_select_folder(self, dialog, path):
        dialog_for_folder = Gtk.FileDialog()
        dialog_for_folder.select_folder(
            self.__window, None, self.__on_single_selected,
            path
        )

    def __switch_change(self, widget, _, data):
        mode = USER
        if data == "symbolic":
            mode = self.__window.settings.get_mode_symb()
        elif data == "copy":
            mode = self.__window.settings.get_mode_copy()
        elif data == "archive":
            mode = self.__window.settings.get_mode_archive()

        if mode == USER:
            self.__window.cg.set_configuration(data, widget.get_active())
            self.__window.cg.save_plugin()

    def enable_windows(self, activate: bool):
        self.prefix_row.set_visible(activate)

    def set_copie_row(self, activate: bool):
        self.copie_row.set_active(activate)

    def set_symbolic_row(self, activate: bool):
        self.symbolic_row.set_active(activate)

    def set_archive_row(self, activate: bool):
        self.archive_row.set_active(activate)

    def set_path_row(self, path: str):
        subtitle = f'Chemin du jeux : {path}'
        self.path_row.set_subtitle(subtitle)

    def set_prefix_row(self, path: str):
        subtitle = f'Chemin du prefix : {path}'
        self.prefix_row.set_subtitle(subtitle)

    def path_state(self, state):
        self.__path_stape_row.choose_state(state)

    def post_traitement_state(self, state):
        self.__configure_stape_row.choose_state(state)
