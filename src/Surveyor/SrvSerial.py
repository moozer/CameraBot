'''
Created on 3 Dec 2012

@author: moz
'''
from serial.serialutil import SerialException
import serial
import time
import os.path

class TimeoutWarning( Warning ):
    pass

class SrvSerial(serial.Serial):
    ''' handles single threaded communication with surveyor srv-1
    '''
    
    _SendWait = 0.1 # wait this long after each send to the device.
    
    def __init__(self, SrvSerialDevice, Timeout = 0.1):
        ''' @param SrvSerialDeviceLocal: The serial device to use 
        '''
        
#        if not os.path.exists(SrvSerialDevice):
#            raise SerialException("Nonexistent device %s" % (SrvSerialDevice, ) )

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
            raise SerialException( "Init failed. Is the robot turned on?")
        pass

    

    def SendCommand(self, Command ):
        # clean up and send command
        self.flush()
        time.sleep(self._SendWait)
        self.write(Command)
        time.sleep(self._SendWait)

        # check for proper return value
        # We expect something like '#Version ....'
        r = self.read(4096) # read everything until timeout
        if len(r) == 0:
            raise TimeoutWarning
        if r[0] != '#':
            raise SerialException("Bad response received: Expected '%s' got '%s'" % ('#', r))
        
        return r[1:]

    def GetVersion(self):
        # and read the rest (untill timeout)
        self._version = self.SendCommand( 'V' )
        

    # ---------- movement --------------------
    
    def GoForward(self):
        self.SendCommand( '8' )
        pass

    def GoBack(self):
        self.SendCommand( '2' )
        pass

    def GoLeft(self):
        self.SendCommand( '4' )
        pass

    def GoRight(self):
        self.SendCommand( '6' )
        pass

    def Stop(self):
        ''' Issues a stop command to the robot
        '''
        self.SendCommand( '5' )
        pass

    
    # ---------- properties --------------------
        
    @property
    def version(self):
        ''' the version string returned from last version query'''
        return self._version

    
    
    
    


