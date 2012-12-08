'''
Created on 3 Dec 2012

@author: moz

Inspiration:
- http://offkilterengineering.com/using-python-and-wxpython-to-display-a-motion-jpeg-from-the-trendnet-wireless-internet-camera/

'''
import wx
from GUI.wxCameraPanel import CameraPanel

from Surveyor.SrvThread import SrvControl
#from DummyBot.DummyBot import DummyBot
from Controller.JoystickController import JoystickController


if __name__ == '__main__':

    app = wx.App(0)
    wx.Log_SetActiveTarget(wx.LogStderr())
    frame = wx.Frame(parent=None, id=wx.ID_ANY, title='UpCam.py', style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)

    robot = SrvControl("/dev/ttyUSB0")
    #robot = DummyBot()
    
    ctrl = JoystickController( robot )
    
    # visual stuff
    campanel = CameraPanel(frame, robot)
    campanel.SetSize(robot.image.size)

    # main frame
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(campanel, 1, wx.EXPAND|wx.ALL, 5)
    frame.SetSizer(sizer)
    frame.Fit()
    frame.Show(True)

    robot.EnableAcquisition( campanel.Refresh )
    app.MainLoop()