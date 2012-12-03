'''
Created on 3 Dec 2012

@author: moz
'''
import unittest
from Surveyor.SrvSerial import *


SrvSerialDeviceLocal = "SocatTmpSerialLocal"
#SrvSerialDeviceRobot = "SocatTmpSerialRobot"

class Test(unittest.TestCase):

#    def setUp(self):
#        
#    def tearDown(self):
#        

    def testContruction(self):
        s = SrvSerial( SrvSerialDeviceLocal )
        self.assertEqual( s.GetPort(), SrvSerialDeviceLocal )
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testContruction']
    unittest.main()