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
    
    _ContinueLoop = threading.Event()   # if set, continue looping.
    _DoAcquisition = threading.Event()  # if set, do acquisition as fast as possible
    _AcqisitionCallback = None          # hold the callback to call whenever a new image is available
    _CurrentDirection = [0,0]           # neutral position
    _Image = Image.new("RGB", _DEFAULTIMAGESIZE, "white")  # the latest image retrieved. 
    _NextDirection = None               # will attempt to set netxdirection untill it is None

    # wait times for the serial module 
    # for SrvCli, 0.4/0.4 is the best for
    _WAITTIME = 0.5
    _READTIMEOUT = 0.5

    def __init__(self, port = "/dev/ttyUSB0" ):
        ''' Constructor, opens connection and starts the loop '''
        self._SrcConnection = SrvSerial( port, self._WAITTIME, self._READTIMEOUT )
        self._ContinueLoop.clear()
        self._DoAcquisition.clear()
        self.StartLoop()

    def StartLoop(self):
        ''' Loop control, starts the acquisition and command loop '''
        self._ContinueLoop.set()
        self._SrvThread = threading.Thread(target=self._loop, name="SrvControl")
        self._SrvThread.daemon = True 
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
        ''' Disable retrieval of images from the SRV '''
        self._DoAcquisition.clear()

    @property
    def image(self):
        ''' the last image (as PIL.image) '''
        return self._Image
    

    def _ChangeDirection(self, NextDirection):
        ''' get the axis [x,y] values and sets the appropriate 1..9 value in the SRV '''
        Directions = [['7', '4', '1'], 
                      ['8', '5', '2'], 
                      ['9', '6', '3'] ]

        self._SrcConnection.SendCommand( Directions[ int(NextDirection[0])+1][int(NextDirection[1])+1] )
        pass
    
    
    def _loop(self):
        ''' the command loop
        This function is the only one using the SrvSerial object, so no need for locks
        '''
        while( self._ContinueLoop.isSet() ):
            # first: set new direction if any
            if self._NextDirection:
                try:
                    self._ChangeDirection( self._NextDirection )
                    self._CurrentDirection = self._NextDirection
                    self._NextDirection = None
                except Warning, w:
                    print >> sys.stderr, "Warning setting direction (will retry): %s"%w
                except Exception, e:
                    print >> sys.stderr, "Error setting direction (will retry): %s"%e
                
                continue

            # retrieve new image
            if self._DoAcquisition.isSet():              
                try:
                    self._SrcConnection.GetImage()

                    stream = StringIO.StringIO( self._SrcConnection.image )
                    image = Image.open(stream)
                    self._Image = image
                    self._AcqisitionCallback()
                except Exception, e:
                    print >> sys.stderr, "Exception caught (%s): %s"%(type(e), e.message)
                continue

    @property
    def direction(self):
        ''' the last set direction '''
        return self._CurrentDirection
    
    def SetDirection(self, Direction ):
        ''' Sets a new direction
        This sets an internal flag, which the command loop picks up.
        '''
        if Direction == self._CurrentDirection:
            return 
        
        if(     ( Direction[0] > 1 or Direction[0] < -1 )
             or ( Direction[1] > 1 or Direction[1] < -1 ) ):
            raise ValueError( "Directions must be -1 <= 0 <= 1. Direction specified %s"%Direction)

        # I think this is ok from a multithread perspective since = is an atomic operation in python
        self._NextDirection = Direction
            