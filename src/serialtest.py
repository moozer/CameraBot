'''
Created on 29 Nov 2012

@author: moz
'''
import serial
from serial.serialutil import SerialException

class TimeoutWarning( Warning ):
    pass

class SurveyorSerial( serial ):
    _timeout = 1 # default no of seconds for timeout
    
    def __init__(self, port):
        super(serial, self).__init__(
              port=port,
              baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              timeout=self._timeout, # timeout value in seconds, None for forever
              xonxoff=0, rtscts=0 )

        self._port = port
        
        try:
            self.GetVersion()
        except TimeoutWarning:
            raise SerialException
        
    def GetPort(self):
        '''
        returns the port currently used.
        '''
        return self._port

    def GetVersion(self):
        self.write('V')
        
        # check
        if not self.read() == '#':
            raise TimeoutWarning
        
        
        
        pass
        

s = SurveyorSerial( "/dev/ttyUSB0" )
