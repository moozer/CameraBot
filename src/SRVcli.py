'''
Created on 27 Nov 2012

@author: moz
'''
from Surveyor.SrvSerial import SrvSerial
import time

ComPort = "/dev/ttyUSB0"

if __name__ == '__main__':
    print "Connecting"
    s = SrvSerial( ComPort )
    
    # move around a bit
    s.GoForward()
    time.sleep( 2 )
    s.GoBack()
    time.sleep( 2 )
    s.Stop()
#    s.capture_frame()
#    print s.get_jpeg()
    
    print "The end"

    