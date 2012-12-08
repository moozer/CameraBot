'''
Created on 8 Dec 2012

@author: moz

Inspiration:
- http://offkilterengineering.com/using-python-and-wxpython-to-display-a-motion-jpeg-from-the-trendnet-wireless-internet-camera/
- http://jehiah.cz/a/pil-to-wxbitmap
'''
import wx
import StringIO
import sys
import PIL

class CameraPanel(wx.Panel):

    def __init__(self, parent, camera):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=wx.SIMPLE_BORDER)
        self._Camera = camera
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        try:
            if self._Camera.image  != None:
                pilImage = self._Camera.image
                
                wximage = wx.EmptyImage(pilImage.size[0],pilImage.size[1])
                wximage.SetData(pilImage.convert("RGB").tostring())
                wximage.SetAlphaData(pilImage.convert("RGBA").tostring()[3::4] )
                
                bmp = wx.BitmapFromImage( wximage)
                dc.DrawBitmap(bmp, 0, 0, True)
        except Exception, e:
            print >> sys.stderr, "Exception while reading image: %s"%e
            pass

