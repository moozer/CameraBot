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
    _NextDirection = None

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
    

    def _ChangeDirection(self, NextDirection):
        Directions = [['7', '4', '1'], 
                      ['8', '5', '2'], 
                      ['9', '6', '3'] ]
        #{ '(-1,1)'  : "7",  '(0,1)'  : "8",  '(1,1)'  : "9",
        #               '(-1,0)'  : "4",  '(0,0)'  : "5",  '(1,0)'  : "6",
        #               '(-1,-1)' : "1",  '(0,-1)' : "2",  '(1,-1)' : "3"
        #               }
        
#        if not str(NextDirection) in Directions:
#            OutStr = "Unknown direction: %s"%NextDirection
#            NextDirection = None
#            raise ValueError( OutStr )

        self._SrcConnection.SendCommand( Directions[ int(NextDirection[0])+1][int(NextDirection[1])+1] )
        pass
    
    
    def _loop(self):
        ''' the command loop
        This function is the only one using the SrvSerial object, so no need for locks
        '''
        while( self._ContinueLoop.isSet() ):
            if self._NextDirection:
                try:
                    self._ChangeDirection( self._NextDirection )
                    self._CurrentDirection = self._NextDirection
                    self._NextDirection = None
                except Exception, e:
                    print >> sys.stderr, "Error setting direction (will retry): %s"%e
                except Warning, w:
                    print >> sys.stderr, "Warning setting direction (will retry): %s"%w
                
                continue
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

    @property
    def direction(self):
        return self._CurrentDirection
    
    def SetDirection(self, Direction ):
        if Direction == self._CurrentDirection:
            return 
        
        if(     ( Direction[0] > 1 or Direction[0] < -1 )
             or ( Direction[1] > 1 or Direction[1] < -1 ) ):
            raise ValueError( "Directions must be -1 <= 0 <= 1. Direction specified %s"%Direction)

        # I think this is ok from a multithread perspective since = is an atomic operation in python
        self._NextDirection = Direction
            