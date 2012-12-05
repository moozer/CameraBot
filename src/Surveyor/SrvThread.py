'''
Created on 5 Dec 2012

@author: moz
'''
from Surveyor.SrvSerial import SrvSerial
import threading
import sys

class SrvControl( object ):
    _ContinueLoop = threading.Event()  # if set, continue looping.
    _DoAcquisition = threading.Event() # if set, do acquisition as fast as possible
    _AcqisitionCallback = None # hold the callback to call whenever a new image is available
    _LastestImage = None       # the latest image retrieved. Could be initialized with something cool :-) 
    
    def __init__(self, port = "/dev/ttyUSB0" ):
        self._SrcConnection = SrvSerial( port )
        self._ContinueLoop.clear()
        self._DoAcquisition.clear()

    def StartLoop(self):
        ''' Loop control, starts the acquisition and command loop '''
        self._ContinueLoop.set()
        self._SrvThread = threading.Thread(target=self._loop)
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
        return self._LastestImage
    
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
                    self._LastestImage = self._SrcConnection.image
                    self._AcqisitionCallback()
                except Exception, e:
                    print >> sys.stderr, "Exception caught (%s): %s"%(type(e), e.message)
                continue

            