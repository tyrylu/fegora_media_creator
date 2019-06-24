import wx
from . import main_controller

def main():
    app = wx.App()
    mc = main_controller.MainController()
    mc.show_window()
    app.MainLoop()  