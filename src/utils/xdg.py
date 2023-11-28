import os
import xdg.BaseDirectory

def xdg_conf_path():
    conf_path = "~/"
    try:
        conf_path = xdg.BaseDirectory.xdg_config_home
    except:
        print("Error no XDG Conf define")

    conf_path = os.path.join(conf_path, "linux_mode_manager")

    if not os.path.isdir(conf_path):
        os.makedirs(conf_path)

    return conf_path