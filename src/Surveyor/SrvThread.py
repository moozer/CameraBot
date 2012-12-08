'''
Created on 5 Dec 2012

@author: moz
'''
from Surveyor.SrvSerial import SrvSerial
import threading
import sys
import Image
import StringIO

class SrvControl( object ):
    _DEFAULTIMAGESIZE = (180, 180)
    
    _ContinueLoop = threading.Event()  # if set, continue looping.
    _DoAcquisition = threading.Event() # if set, do acquisition as fast as possible
    _AcqisitionCallback = None # hold the callback to call whenever a new image is available
    _CurrentDirection = [0,0] # neutral position
    _Image = Image.new("RGB", _DEFAULTIMAGESIZE, "white")  # the latest image retrieved. 

    def __init__(self, port = "/dev/ttyUSB0" ):
        self._SrcConnection = SrvSerial( port )
        self._ContinueLoop.clear()
        self._DoAcquisition.clear()
        self.StartLoop()

    def StartLoop(self):
        ''' Loop control, starts the acquisition and command loop '''
        self._ContinueLoop.set()
        self._SrvThread = threading.Thread(target=self._loop, name="SrvControl")
        self._SrvThread.start()

    def StopLoop(self):
        ''' Loop control, ends the acquisition and command loop '''
        self._ContinueLoop.clear()

    def EnableAcquisition(self, callback = None):
        ''' When looping, enable image acquisition - not timed, just as fast as possible
        @param callback: The function to call whenever a new image is available
        '''
        self._AcqisitionCallback = callback
        self._DoAcquisition.set()
        
    def DisableAcquisition(self):
        self._DoAcquisition.clear()

    @property
    def image(self):
        return self._Image
    
    def _loop(self):
        ''' the command loop
        This function is the only one using the SrvSerial object, so no need for locks
        '''
        while( self._ContinueLoop.isSet() ):
#            if NextCommand:
#                Issue( NextCommand )
#                continue
#    
            if self._DoAcquisition.isSet():              
                try:
                    self._SrcConnection.GetImage()

#                    -        stream = StringIO.StringIO( self.RobotCtl.image )
#-        if stream != None:
#-            img = wx.ImageFromStream(stream)
#-            bmp = wx.BitmapFromImage(img)
#-            dc.DrawBitmap(bmp, 0, 0, True)

#                    self._LastestImage = self._SrcConnection.image
                    stream = StringIO.StringIO( self._SrcConnection.image )
                    image = Image.open(stream)
                    self._Image = image
                    self._AcqisitionCallback()
                except Exception, e:
                    print >> sys.stderr, "Exception caught (%s): %s"%(type(e), e.message)
                continue

            