'''
Created on 27 Nov 2012

@author: moz
'''

from Surveyor.SrvSerial import SrvSerial
import time
from Surveyor.SrvThread import SrvControl


def DoSimpleSerial(ComPort):
    ''' this uses the underlying com interface '''
    print "Connecting"
    s = SrvSerial(ComPort, 0.5)
# move around a bit
    s.GoForward()
    time.sleep(2)
    s.GoBack()
    time.sleep(2)
    s.Stop()
    img = s.GetImage()
    f = open('nn.jpeg', 'w+')
    f.write(img)
    f.close()
    print "The end"

ComPort = "/dev/ttyUSB1"

ImageCount = 0

def AcqCallback():
    global ImageCount
    ImageCount += 1
    print "Image acquired: %d"%ImageCount
    
def DoThreadedConnection(ComPort):
    print "Multithread version"
    
    s = SrvControl(ComPort)
    s.EnableAcquisition( AcqCallback )
    
    
    print "just sleeping now."
    time.sleep(10)
#    s.StopLoop()
    
    print "The End"
    


if __name__ == '__main__':
    print "simple serial"
#    DoSimpleSerial(ComPort)
    print "simple serial ended"


    print "threaded serial"
    DoThreadedConnection( ComPort )
    print "threaded serial ended"
    