import wx
from . import size_utils

class MainWindow(wx.Frame):

    def __init__(self):
        super().__init__(None, -1, _("Fegora media creator"))
        self._panel = wx.Panel(self, -1)
        self._sizer = wx.GridBagSizer(2)
        self._disk_label = wx.StaticText(self._panel, -1, _("Select the disk to use"))
        self._disk_choice = wx.Choice(self._panel, -1)
        self.start_button = wx.Button(self._panel, -1, _("Create media"))
        self._sizer.Add(self._disk_label, pos=(0, 0))
        self._sizer.Add(self._disk_choice, (0, 1))
        self._sizer.Add(self.start_button, pos=(1, 0), span=(0, 2))
        self._panel.SetSizer(self._sizer)

    def add_disk(self, disk):
        self._disk_choice.Append(f"{disk.caption}: {size_utils.format_size(disk.size)}")

    @property
    def selected_disk_index(self):
        return self._disk_choice.Selection
