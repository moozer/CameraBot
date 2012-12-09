'''
Created on 3 Dec 2012

@author: moz
'''
import unittest
from Surveyor.SrvSerial import *
from subprocess import Popen
import serial
import time
import string
import sys
from unittest.case import SkipTest

SrvSerialDeviceLocal = "SocatTmpSerialLocal"
SrvSerialDeviceRobot = "SocatTmpSerialRobot"

# Socat command for ouputting data transferred to stderr
#SocatCmdLine = ["/usr/bin/socat", "-x", "-v", "PTY,link=%s"%(SrvSerialDeviceLocal,), "PTY,link=%s"%(SrvSerialDeviceRobot,)]

SocatCmdLine = ["/usr/bin/socat", "PTY,link=%s"%(SrvSerialDeviceLocal,), "PTY,link=%s"%(SrvSerialDeviceRobot,)]
TimeoutTime = 0.5
EchoCmd = ['python', 'EchoMachine.py']

class Test(unittest.TestCase):

    def setUp(self):
        # for test debugging
        #print >> sys.stderr, "%s"%string.join(SocatCmdLine, " ")
        self._SocatPopen = Popen(SocatCmdLine)
        time.sleep( TimeoutTime )
        self._EchoPopen = Popen( EchoCmd )

    def tearDown(self):
        self._SocatPopen.kill()
        self._EchoPopen.kill()
        pass

    def testPipe(self):
        self._EchoPopen.kill()

        SerConnA = serial.Serial(
              port=SrvSerialDeviceLocal,
              baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              timeout=0, # timeout value in seconds, None for forever
              xonxoff=0, rtscts=0)
        SerConnA.flush()
        
        SerConnB = serial.Serial(
              port=SrvSerialDeviceRobot,
              baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              timeout=0, # timeout value in seconds, None for forever
              xonxoff=0, rtscts=0)
        SerConnB.flush()
        
        testData = "abc\n"
        SerConnA.write(testData)
        time.sleep( TimeoutTime )
        OutData = SerConnB.read(len(testData) )
        self.assertEqual(testData, OutData )
                          
        SerConnB.write(testData)
        time.sleep( TimeoutTime )
        OutData = SerConnA.read(len(testData) )
        self.assertEqual(testData, OutData )

    def testPipeEcho(self):
        SerConnA = serial.Serial(
              port=SrvSerialDeviceLocal,
              baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              timeout=0, # timeout value in seconds, None for forever
              xonxoff=0, rtscts=0)
        SerConnA.flush()
        time.sleep( TimeoutTime)
        
        testData="a"

        SerConnA.write(testData)
        time.sleep( TimeoutTime )
        OutData = SerConnA.read(2)
            
        self.assertEqual( OutData, "#%s"%testData)

    def testConnection(self):
        s = SrvSerial( SrvSerialDeviceLocal )
        self.assertEqual( s.port, SrvSerialDeviceLocal )     
        self.assertEqual( s.version, 'V' ) # bogus Version 
        pass
    
    def testForwardLeftRightBackStop(self):
        s = SrvSerial( SrvSerialDeviceLocal )
        s.GoForward()
        s.GoBack()
        s.GoLeft()
        s.GoRight()
        s.GoLeft()
        s.Stop()
        pass

    def testNoConnection(self):
        self._SocatPopen.kill()
        time.sleep( 0.3 )
        self.assertRaises(SerialException, SrvSerial, SrvSerialDeviceLocal)

    def testNoEcho(self):
        self._EchoPopen.kill()
        time.sleep( 0.3 )
        self.assertRaises(SerialException, SrvSerial, SrvSerialDeviceLocal )
        
    def testGetImage(self):
        s = SrvSerial( SrvSerialDeviceLocal )
        # the echo machine cannot handle sending images.
        self.assertRaises( SerialException, s.GetImage )
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testContruction']
    unittest.main()