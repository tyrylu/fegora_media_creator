import wx
from . import main_window
from . import disk_utils
from . import server_interaction
from . import local_storage
from .size_utils import format_size


class MainController:

    def __init__(self):
        self._download_progress_dialog = None
        self._disks = disk_utils.get_removable_disks()
        self._window = main_window.MainWindow()
        self._window.start_button.Bind(wx.EVT_BUTTON, self._on_start)
    
    def show_window(self):
        for disk in self._disks:
            self._window.add_disk(disk)
        self._window.Show()

    def _on_start(self, evt):
        server_checksum = server_interaction.get_image_checksum()
        if not local_storage.image_checksum_is_current(server_checksum):
            if not server_interaction.download_image(local_storage.IMAGE_FILE, self._download_progress_callback):
                wx.MessageBox(_("Failed to download the image."), _("Error"), style=wx.ICON_ERROR)
                return
            local_storage.update_checksum(server_checksum)
    
    def _download_progress_callback(self, total, so_far):
        if not self._download_progress_dialog:
            self._download_progress_dialog = wx.ProgressDialog(_("Download in progress"), _("Downloading the image."), parent=self._window, style=wx.PD_APP_MODAL|wx.PD_ESTIMATED_TIME|wx.PD_AUTO_HIDE)
        percentage = int((so_far/total)*100)
        self._download_progress_dialog.Update(percentage, _("Downloading the image. Downloaded {so_far} of {total}.").format(so_far=format_size(so_far), total=format_size(total)))

    