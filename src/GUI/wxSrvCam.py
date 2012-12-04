'''
Created on 3 Dec 2012

@author: moz

This one is from
http://offkilterengineering.com/using-python-and-wxpython-to-display-a-motion-jpeg-from-the-trendnet-wireless-internet-camera/

'''
import StringIO
import threading
import time
import wx
from Surveyor.SrvSerial import SrvSerial, TimeoutWarning
import sys

class CameraPanel(wx.Panel):

    def __init__(self, parent, camera):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=wx.SIMPLE_BORDER)
        self.Camera = camera
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        try:
            stream = StringIO.StringIO( self.Camera.GetImage() )
            if stream != None:
                img = wx.ImageFromStream(stream)
                bmp = wx.BitmapFromImage(img)
                dc.DrawBitmap(bmp, 0, 0, True)
        except TimeoutWarning:
            print >> sys.stderr, "Timeout reading image data"
            pass


if __name__ == '__main__':

    def CamThread():
        while True:
            campanel.Refresh()
            time.sleep(.1)
    
    app = wx.App(0)
    wx.Log_SetActiveTarget(wx.LogStderr())
    frame = wx.Frame(parent=None, id=wx.ID_ANY, title='UpCam.py', style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
    camera = SrvSerial("/dev/ttyUSB0")
    
    campanel = CameraPanel(frame, camera)
    campanel.SetSize((620,480))

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(campanel, 1, wx.EXPAND|wx.ALL, 5)
    frame.SetSizer(sizer)
    frame.Fit()
    frame.Show(True)

    thread = threading.Thread(target=CamThread)
    thread.start()

    app.MainLoop()