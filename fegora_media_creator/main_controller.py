from . import main_window
from . import disk_utils

class MainController:

    def __init__(self):
        self._disks = disk_utils.get_removable_disks()
        self._window = main_window.MainWindow()
    
    def show_window(self):
        for disk in self._disks:
            self._window.add_disk(disk)
        self._window.Show()