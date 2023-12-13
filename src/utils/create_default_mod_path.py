import os
from utils.xdg import xdg_share_path

def create_default_mod_path(settings):
    path = xdg_share_path()

    folders = [
        ["download", 'donwload-base-folder'],
        ["archive", 'archive-base-folder'],
        ["installed", 'install-base-folder']
    ]

    for folder, setting_name in folders:
        final_folder = str()
        path_setting = settings.get_string(setting_name)
        if not path_setting == "":
            final_folder = path_setting
        else:
            final_folder = os.path.join(path, folder)
        if not os.path.isdir(final_folder):
            os.makedirs(final_folder)
            settings.set_string(setting_name, final_folder)
