'''
Created on 27 Nov 2012

@author: moz
'''
from SRVcom import Srv1

ComPort = "/tmp/serial"

if __name__ == '__main__':
    s = Srv1( ComPort, False )
    
    print "Connecting"
    s.connect()
    if not s.is_connected():
        print "failed to connect"
        exit() 
    
    print "Name is", s.getName()
    
    s.capture_frame()
    print s.get_jpeg()
    
    print "Disconnecting"
    s.disconnect()
    