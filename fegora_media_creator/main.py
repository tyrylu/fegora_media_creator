import wx
from . import main_controller
from . import locale_setup
import elevate

def main():
    elevate.elevate()
    app = wx.App()
    locale_setup.setup_locale()
    mc = main_controller.MainController()
    mc.show_window()
    app.MainLoop()  