'''
Created on 3 Dec 2012

@author: moz
'''
from serial.serialutil import SerialException
import serial
import time
from struct import unpack

class TimeoutWarning( Warning ):
    pass

class SrvSerial(serial.Serial):
    ''' handles single threaded communication with surveyor srv-1
    '''
    
    _version = None # the version string
    _image = None   # holds the last image retrieved

    # set in constructor
    _MaxRetries = 3 # wait for timeout multiple times (default: 3)
    _Timeout = 1 # wait this long for response (default: 1 sec, ie. very conservative)
    _SendWait = 1 # wait this long after each send to the device. (default: 1 sec, ie. very conservative)

    def __init__(self, SrvSerialDevice, Timeout = 0.3, SendWait = 0.3):
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
        self._SendWait = SendWait

        try:
            self.GetVersion()
        except TimeoutWarning:
            raise SerialException( "Init failed. Is the robot turned on?")
    

    def SendCommand(self, Command ):
        # clean up and send command
        self.flush()
        time.sleep(self._SendWait) # if this is excluded, you see your own transmits ?!
        self.write(Command)
        time.sleep(self._SendWait)

        # check for proper return value
        # We expect something like '#%s'%Command
        Retries = 0
        while True:
            r = self.read(4096) # read everything until timeout
            if len(r) == 0:
                Retries += 1
                if Retries > self._MaxRetries:
                    raise TimeoutWarning( "Timeout after %d retries"%(Retries-1) )
                else:
                    continue
            if r[0] != '#':
                raise SerialException("Bad response received: Expected '%s' got '%s'" % ('#', r))
            
            # no probs? then continue
            break
        
        return r[1:]


    # ---------- Specific commands --------------------

    def GetVersion(self):
        # and read the rest (untill timeout)
        self._version = self.SendCommand( 'V' ) 
    
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

    def GetImage(self):
        ''' from the docs
        Command : 'I' grab JPEG compressed video frame
        Returns : '##IMJxs0s1s2s3....'     
            x = frame size in pixels: 1 = 80x64, 3 = 160x120, 5 = 320x240, 7 = 640x480, 9 = 1280x1024 
            s0s1s2s3=frame size in bytes (s0 * 256^0 + s1 * 256^1 + s2 * 256^2 + s3 * 256^3) 
            .... = full JPEG frame 

        Note that sometimes the 'I' command returns nothing if the robot camera is busy, 
        so the 'I' command should be called as many times as needed until a frame is returned
        '''
        
        data = self.SendCommand('I')

        #self.srvConn.timeout = .25
        #head = self.srvConn.read(10);
        if (len(data) < 10 or not(data[0:4] == '#IMJ')):
            self.flushInput()
            self.flushOutput()
            raise SerialException( "Failed to read image header: '%s'"%data[:9] )

        # process header info
        frameHead = unpack('<cHxx', data[4:9])
        
        #ImageResolution = frameHead[0]
        ImageSize = frameHead[1]

        if len(data) < ImageSize+9:
            data += self.read()
            
        self._image = data[9:]
        return self._image

    
    # ---------- properties --------------------
        
    @property
    def version(self):
        ''' the version string returned from last version query'''
        return self._version

    @property
    def image(self):
        ''' the latest image
        @return: Image or None if no image has yet been received
        '''
        return self._image
    
    
    


