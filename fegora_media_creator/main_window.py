import wx
from bitmath import Byte

class MainWindow(wx.Frame):

    def __init__(self):
        super().__init__(None, -1, "Fegora media creator")
        self._panel = wx.Panel(self, -1)
        self._sizer = wx.GridBagSizer(2)
        self._disk_label = wx.StaticText(self._panel, -1, "Select the disk to use")
        self._disk_choice = wx.Choice(self._panel, -1)
        self._start_button = wx.Button(self._panel, -1, "Create media")
        self._sizer.Add(self._disk_label, pos=(0, 0))
        self._sizer.Add(self._disk_choice, (0, 1))
        self._sizer.Add(self._start_button, pos=(1, 0), span=(0, 2))
        self._panel.SetSizer(self._sizer)

    def add_disk(self, disk):
        size_str = Byte(disk.size).best_prefix().format("{value:.2f} {unit}")
        self._disk_choice.Append(f"{disk.caption}: {size_str}")