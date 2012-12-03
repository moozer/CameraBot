'''
Created on 3 Dec 2012

@author: moz
'''
from serial.serialutil import SerialException
import serial
import time

class TimeoutWarning( Warning ):
    pass

class SrvSerial(serial.Serial):
    ''' handles single threaded communication with surveyor srv-1
    '''
    
    _SendWait = 0.3 # wait this long after each send to the device.
    
    def __init__(self, SrvSerialDevice, Timeout = 0.3):
        ''' @param SrvSerialDeviceLocal: The serial device to use 
        '''
        # init serial connection
        super(SrvSerial, self).__init__(
              port=SrvSerialDevice,
              baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              timeout=Timeout, # timeout value in seconds, None for forever
              xonxoff=0, rtscts=0 )
        
        # save class vars
        self._Timeout = Timeout

        try:
            self.GetVersion()
        except TimeoutWarning:
            raise SerialException
        pass

    
    def GetVersion(self):
        # clean up and send command
        self.flush()
        time.sleep( self._SendWait)
        self.write('V')
        time.sleep( self._SendWait)
        
        # check for proper return value
        # We expect something like '#Version ....'
        r = self.read(4096) # read everything until timeout

        if len(r) == 0:
            raise TimeoutWarning

        if r[0] != '#':
            raise SerialException( "Bad response received: Expected '%s' got '%s'"%('#', r))
        
        # and read the rest (untill timeout)
        self._version = r[1:]
        
    
    # ---------- properties --------------------
        
    @property
    def version(self):
        ''' the version string returned from last version query'''
        return self._version
    
    


