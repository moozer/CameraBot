'''
Created on 3 Dec 2012

@author: moz
'''
import unittest
from Surveyor.SrvSerial import *
from subprocess import Popen
import serial
import time


SrvSerialDeviceLocal = "SocatTmpSerialLocal"
SrvSerialDeviceRobot = "SocatTmpSerialRobot"
SocatCmdLine = ["/usr/bin/socat", "-x", "-v", "PTY,link=%s"%(SrvSerialDeviceLocal,), "PTY,link=%s"%(SrvSerialDeviceRobot,)]

class Test(unittest.TestCase):

    def setUp(self):
        self._SocatPopen = Popen(SocatCmdLine)
        print self._SocatPopen
        time.sleep( 0.5 )

    def tearDown(self):
        self._SocatPopen.kill()

    def testPipe(self):
        SerConnA = serial.Serial(
              port=SrvSerialDeviceLocal,
              baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              timeout=0, # timeout value in seconds, None for forever
              xonxoff=0, rtscts=0)

        SerConnB = serial.Serial(
              port=SrvSerialDeviceRobot,
              baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              timeout=0, # timeout value in seconds, None for forever
              xonxoff=0, rtscts=0)

        testData = "abc\n"
        SerConnA.write(testData)
        time.sleep( 0.5 )
        OutData = SerConnB.read(len(testData) )
        self.assertEqual(testData, OutData )
                          
        SerConnB.write(testData)
        time.sleep( 0.5 )
        OutData = SerConnA.read(len(testData) )
        self.assertEqual(testData, OutData )

    def testContruction(self):
        s = SrvSerial( SrvSerialDeviceLocal )
        self.assertEqual( s.GetPort(), SrvSerialDeviceLocal )
        pass

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testContruction']
    unittest.main()