'''
Created on 3 Dec 2012

@author: moz
'''
import unittest
from Surveyor.SrvSerial import *
from subprocess import Popen
import serial
import time
import os


SrvSerialDeviceLocal = "SocatTmpSerialLocal"
SrvSerialDeviceRobot = "SocatTmpSerialRobot"
SocatCmdLine = ["/usr/bin/socat", "-x", "-v", "PTY,link=%s"%(SrvSerialDeviceLocal,), "PTY,link=%s"%(SrvSerialDeviceRobot,)]
TimeoutTime = 0.5
EchoCmd = ['python', 'EchoMachine.py']

class Test(unittest.TestCase):

    def setUp(self):
        self._SocatPopen = Popen(SocatCmdLine)
        time.sleep( TimeoutTime )
        self._EchoPopen = Popen( EchoCmd )

    def tearDown(self):
        self._SocatPopen.kill()
        self._EchoPopen.kill()
        pass

#    @unittest.SkipTest
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
        
        print "send start"
        testData="a"

        SerConnA.write(testData)
        time.sleep( TimeoutTime )
        OutData = SerConnA.read(2)
            
        self.assertEqual( OutData, "#%s"%testData)

    @unittest.SkipTest
    def testConnection(self):
        s = SrvSerial( SrvSerialDeviceLocal )
        self.assertEqual( s.GetPort(), SrvSerialDeviceLocal )        
        self.assertEqual(s.GetVersion, 'V' ) # bogus V 
        pass

        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testContruction']
    unittest.main()