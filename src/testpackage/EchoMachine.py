'''
Created on 3 Dec 2012

@author: moz

Inspiration from here:
http://code.activestate.com/recipes/134892/
'''


##This is the simple solution, but the read() doesn't return before a newline is received...
#import sys
#while True:
#    ch = sys.stdin.read(1)
#    print "#%s"%ch


## This fails since we need to pipe stdin and stdout to the same device...
#import sys
#import termios
#import tty
#
#fd = sys.stdin.fileno()
#old_settings = termios.tcgetattr(fd)
#while True:
#    try:
#        tty.setraw(sys.stdin.fileno())
#        ch = sys.stdin.read(1)
#    except:
#        break
#    
#    sys.stdout.write("#%s"%ch)
#    sys.stdout.flush()
#
#
#termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

import serial

SerConn = serial.Serial(
      port="SocatTmpSerialRobot",
      baudrate=115200,
          bytesize=serial.EIGHTBITS,
          parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      timeout=None, # timeout value in seconds, None for forever
      xonxoff=0, rtscts=0)
SerConn.flush()
print "echo start"

while True:
    ch = SerConn.read(1)
    SerConn.write("#%s"%ch)
    print "echoing %s"%ch

    
    
    