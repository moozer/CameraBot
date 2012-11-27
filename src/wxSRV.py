'''
Created on 27 Nov 2012

@author: moz
'''
import wx
import cStringIO

class TopFrame(wx.Frame):
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        panel = ImagePanel(self, -1)

        button = wx.Button(panel, 1003, "Close Me")
        button.SetPosition((15, 15))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


class ImagePanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)

        data = open( '../img/surveyor.gif', "rb").read()
        stream = cStringIO.StringIO(data)

        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))

        wx.StaticText(
            self, -1, "This image was loaded from a Python file-like object:", 
            (15, 15)
            )

        wx.StaticBitmap(self, -1, bmp, (15, 45))#, (bmp.GetWidth(), bmp.GetHeight()))



if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = TopFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()