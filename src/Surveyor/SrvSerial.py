'''
Created on 3 Dec 2012

@author: moz
'''

class SrvSerial(object):
    ''' handles single threaded communication with surveyor srv-1
    '''
    
    def __init__(self, SrvSerialDevice):
        ''' @param SrvSerialDeviceLocal: The serial device to use 
        '''
        self._port = SrvSerialDevice
        pass

    
    def GetPort(self):
        return self._port
    
    


