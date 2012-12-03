'''
Created on 3 Dec 2012

@author: moz

This one is from
http://offkilterengineering.com/using-python-and-wxpython-to-display-a-motion-jpeg-from-the-trendnet-wireless-internet-camera/

'''
import httplib
import base64
import StringIO
import threading
import time
import wx

class Trendnet():

    def __init__(self, ip='1.1.1.1', username='admin', password='admin'):
        self.IP = ip
        self.Username = username
        self.Password = password
        self.Connected = False

    def Connect(self):
        if self.Connected == False:
            try:
                print 'Atempting to connect to camera', self.IP, self.Username, self.Password
                h = httplib.HTTP(self.IP)
                h.putrequest('GET','/cgi/mjpg/mjpeg.cgi')
                h.putheader('Authorization', 'Basic %s' % base64.encodestring('%s:%s' % (self.Username, self.Password))[:-1])
                h.endheaders()
                errcode, errmsg, headers = h.getreply()
                self.File = h.getfile()
                print 'Connected!'
                self.Connected = True
            except:
                print 'Unable to connect!'
                self.Connected = False

def Disconnect(self):
    self.Connected = False
    print 'Camera Disconnected!'

def Update(self):
    if self.Connected:
        s = self.File.readline()    # '--myboundry'
        s = self.File.readline()    # 'Content-Length: #####'
        framesize = int(s[16:])
        s = self.File.read(framesize)  # jpeg data
        while s[0] != chr(0xff):
            s = s[1:]
        return StringIO.StringIO(s)

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
        if self.Camera.Connected == True:
            try:
                stream = self.Camera.Update()
                if stream != None:
                    img = wx.ImageFromStream(stream)
                    bmp = wx.BitmapFromImage(img)
                    dc.DrawBitmap(bmp, 0, 0, True)
            except:
                pass
        else:
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.DrawRectangle(-1, -1, 620, 480)

if __name__ == '__main__':

    def CamThread():
        while True:
            campanel.Refresh()
            time.sleep(.01)
    
    app = wx.App(0)
    wx.Log_SetActiveTarget(wx.LogStderr())
    frame = wx.Frame(parent=None, id=wx.ID_ANY, title='UpCam.py', style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
    camera = Trendnet('192.168.1.102')
    camera.Connect()
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