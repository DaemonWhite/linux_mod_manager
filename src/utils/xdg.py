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


def xdg_share_path():
    share_path = "~/.local/share"
    try:
        share_path = xdg.BaseDirectory.xdg_data_home
    except Exception as e:
        print(f"Error no XDG share define: {e}")

    share_path = os.path.join(share_path, "linux_mode_manager")

    if not os.path.isdir(share_path):
        os.makedirs(share_path)

    return share_path
