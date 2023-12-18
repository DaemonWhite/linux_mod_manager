import os
import shutil
import threading
import copy

class DownloadModManager(object):
    def __init__(self, task_synchrone=1):
        self.__TASK_SYNCHRONE = task_synchrone
        self.__count_task = 0
        self.__count_download = 0
        self.__count_total_download = 0
        self.__count_total_end_download = 0
        self.__list_download_mod = []

        self.__callback_progress = self.__default_callback
        self.__callback_end = self.__default_callback

    @property
    def total_download(self):
        return self.__count_total_download

    @property
    def total_download_end(self):
        return self.__count_total_end_download

    def __default_callback(*args):
        pass

    def set_callback_progress(self, callback):
        self.__callback_progress = callback

    def set_callback_end(self, callback):
        self.__callback_end = callback

    def clear(self):
        self.__count_task = 0
        self.__count_download = 0
        self.__count_total_download = 0
        self.__count_total_end_download = 0
        self.__list_download_mod.clear()

    def verif_exist_files(self, src):
        pass

    def __call_callback_progress(self, progress, *args):
        self.__callback_progress(progress, *args)

    def __call_callback_end(self):
        self.__callback_end(self.total_download_end, self.total_download)

    def __add_task(self):
        if self.__count_task < self.__TASK_SYNCHRONE and self.__count_download > 0 :

            copy_thread = threading.Thread(target=self.__task, args=(self.__list_download_mod[0].copy(),))
            copy_thread.start()
            self.__list_download_mod.pop(0)
            self.__count_download -= 1
            self.__count_task += 1

    def __task(self, task_data):
        task = DownloadMod(task_data['plugin'])
        task.set_src_path(task_data['src'])
        task.set_dest_path(task_data['dest'])
        task.set_progress_callback(self.__call_callback_progress, task_data['object_callback'])
        task.copy()
        self.__count_task -= 1
        self.__count_total_end_download += 1
        self.__call_callback_end()
        self.__add_task()


    def append(self, src: str, dest: str, plugin: str, *args):
        dl_data = {
            'src' : src,
            'dest' : dest,
            'plugin' : plugin,
            'object_callback' : args
        }
        self.__count_download += 1
        self.__count_total_download += 1
        self.__list_download_mod.append(dl_data)
        self.__add_task()

class DownloadMod(object):
    def __init__(self, plugin):
        self.__base_path = str()
        self.__progress_percentage = float()
        self.__dest_path = str()
        self.__name = str()
        self.__src_path = str()
        self.__plugin = plugin

        self.__progress_callback = self.__default_callaback
        self.__args = []

    @property
    def name(self):
        return self.__name

    @property
    def plugin(self):
        return self.__plugin

    @property
    def dest_path(self):
        return self.__dest_path

    @property
    def src_path(self):
        return self.__src_path

    @property
    def progress_percentage(self) -> float:
        return self.__progress_percentage

    def __default_callaback(self, progress, *args):
        print("Progress : ", progress)

    def set_progress_callback(self, callback, *args):
        self.__progress_callback = callback
        self.__args = args

    def set_dest_path(self, path):
        path = os.path.join(path, self.__plugin)
        if not os.path.isdir(path):
            os.makedirs(path)

        self.__dest_path = path

    def set_src_path(self, src: str):
        file = src.split('/')
        file = file[len(file) - 1]
        self.__name = file
        self.__src_path = src

    def download(self, url_path):
        pass

    def __copy(self):
        total_size = os.path.getsize(self.__src_path)
        copied_size = 0
        buffer_size = 1024 * 1024  # 1 MB

        self.__dest_path = os.path.join(self.__dest_path, self.__name)

        with open(self.__src_path, 'rb') as source_file, open( self.__dest_path, 'wb') as dest_file:
            buffer = source_file.read(buffer_size)
            while buffer:
                dest_file.write(buffer)

                copied_size += len(buffer)

                self._progress_percentage = (copied_size / total_size)
                self.__progress_callback(self._progress_percentage, *self.__args)
                buffer = source_file.read(buffer_size)

    def copy(self):
        self.__copy()
