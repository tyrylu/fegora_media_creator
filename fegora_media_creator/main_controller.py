import wx
from . import main_window
from . import disk_utils
from . import server_interaction
from . import local_storage
from .size_utils import format_size


class MainController:

    def __init__(self):
        self._download_progress_dialog = None
        self._write_progress_dialog = None
        self._disks = disk_utils.get_removable_disks()
        self._window = main_window.MainWindow()
        self._window.start_button.Bind(wx.EVT_BUTTON, self._on_start)
    
    def show_window(self):
        for disk in self._disks:
            self._window.add_disk(disk)
        self._window.Show()

    def _on_start(self, evt):
        if self._window.selected_disk_index < 0:
            wx.MessageBox(_("You didn't select a disk to use, please, do so."), _("Select a disk"), style=wx.ICON_ERROR)
            return
        server_checksum = server_interaction.get_image_checksum()
        if not local_storage.image_checksum_is_current(server_checksum):
            if not server_interaction.download_image(local_storage.IMAGE_FILE, self._download_progress_callback):
                wx.MessageBox(_("Failed to download the image."), _("Error"), style=wx.ICON_ERROR)
                return
            local_storage.update_local_checksum(server_checksum)
        disk = self._disks[self._window.selected_disk_index]
        resp = wx.MessageBox(_("Do you really want to continue and write the image to {disk_caption}? Be warned that after this operation all data on {disk_caption} will be irreversibly lost.").format(disk_caption=disk.caption), _("Continue"), style=wx.ICON_QUESTION|wx.YES_NO|wx.NO_DEFAULT)
        if resp == wx.YES:
            try:
                disk_utils.write_image_to(disk, self._write_progress_callback)
            except Exception as e:
                wx.MessageBox(_("The write operation failed, error: {}").format(e), _("Failed to write"), style=wx.ICON_ERROR)
                if self._write_progress_dialog:
                    self._write_progress_dialog.Destroy()
                    self._write_progress_dialog = None
                return
            wx.MessageBox(_("The image has been successfully written."), _("Success"), style=wx.ICON_INFORMATION)
    
    def _download_progress_callback(self, total, so_far):
        if not self._download_progress_dialog:
            self._download_progress_dialog = wx.ProgressDialog(_("Download in progress"), _("Downloading the image."), parent=self._window, style=wx.PD_APP_MODAL|wx.PD_ESTIMATED_TIME|wx.PD_AUTO_HIDE)
        percentage = int((so_far/total)*100)
        self._download_progress_dialog.Update(percentage, _("Downloading the image. Downloaded {so_far} of {total}.").format(so_far=format_size(so_far), total=format_size(total)))

    def _write_progress_callback(self, total, so_far):
        if not self._write_progress_dialog:
            self._write_progress_dialog = wx.ProgressDialog(_("Writing the image"), _("Writing the image."), parent=self._window, style=wx.PD_APP_MODAL|wx.PD_ESTIMATED_TIME|wx.PD_AUTO_HIDE)
        percentage = int((so_far/total)*100)
        self._write_progress_dialog.Update(percentage, _("Writing the image. Written {so_far} of {total}.").format(so_far=format_size(so_far), total=format_size(total)))

    