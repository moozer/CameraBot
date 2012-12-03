'''
Created on 27 Nov 2012

@author: moz

This is taken from the pySRV1Console.py program from surveyor.com
'''

from threading import Thread
import Queue
import time
import binascii
from string import find
import serial
from struct import unpack


def log(message, console=False):
    print "[%s] %s"%(message, time.time() )

# 'callback' class to support blocking commands
# has an optional 'queue' member
class SrvCommand:
    def __init__ (self, cmd):
        self.cmd = cmd

class Srv1(Thread):
    def __init__ (self, comPort, ConnectOnStartup = False ):
        #im = Image.new("RGB",[320,240],(int(s[1:3],16),int(s[3:5],16),int(s[5:7],16)))
        #self.im = Image.new("RGB",[320,240],(random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)))
        #self.angle = 0
        Thread.__init__(self)
        self.commands = Queue.Queue(10)
        self.viewers = [ ]
        self.frame = ''
        self.fw_version = 'Unknown'
        self.comPort = comPort
        self.log = { }
        self.connected = False

        if ConnectOnStartup:
            self.connect()

    def run(self):
        while True:
            try:
                if not self.connected:
                    time.sleep(.2)
                    continue

                if not self.commands.empty():
                    self.srvConn.flushInput()
                    self.srvConn.flushOutput()

                while not self.commands.empty():
                    c = self.commands.get(False)

                    # flash write command requires a 500ms delay between zw and the data
                    if c.cmd.startswith('zw'):
                        self.srvConn.write(c.cmd[0:2])
                        time.sleep(.5)
                        self.srvConn.write(c.cmd[2:len(c.cmd)])
                    else:
                        self.srvConn.write(c.cmd)

                    self.srvConn.timeout = .3
                    reply = self.srvConn.read(4096)

                    # chop off everything after the first null
                    first_null = find(reply, binascii.a2b_hex('ff'))
                    if first_null != -1:
                        reply = reply[0:first_null]

                    if hasattr(c, 'queue'):
                        c.queue.put_nowait(reply)

                    #log('Command: ' + c.cmd + ', first occurrence of null: %s' % find(reply, binascii.a2b_hex('ff')))
                    log('Command: ' + c.cmd + ', response: ' + reply)
                    if c.cmd == 'V' and len(reply) > 0:
                        self.fw_version = reply  # cache version string

                # grab / enqueue a frame
                #str = StringIO.StringIO()
                #self.im = self.im.rotate(self.angle)
                #self.angle += 5
                #self.im.save(str, "JPEG")
                #self.frame = str.getvalue()

                self.capture_frame()

                for q in self.viewers:
                    try:
                        if (self.frame != None):
                            q.put_nowait(self.frame)
                    except:
                        pass
            except Exception, e:
                print 'run!', e
                self.disconnect()
                pass

    def connect(self):
        if self.connected:
            log("Already connected to SRV-1", True)
            return

        try:
            self.srvConn = serial.Serial(
              port=self.comPort,
              baudrate=115200,
                  bytesize=serial.EIGHTBITS,
                  parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              timeout=0, # timeout value in seconds, None for forever
              xonxoff=0, rtscts=0)

            self.connected = True
            self.send_command('56')  # 'V' - get version
            log("Connected to SRV-1", True)
        except Exception, inst:
            self.connected = False
            log(str(inst), True)
    def disconnect(self):
        if not self.connected:
            log("Not connected to SRV-1", True);
            return

        try:
            self.srvConn.close()
            self.connected = False
        except:
            pass
        log("Disconnected from SRV-1", True);
    def capture_frame(self):
        try:
            #if (self.srvConn.inWaiting() < 10):
            self.srvConn.write('I')

            #print('available %d' % (self.srvConn.inWaiting()))
            self.srvConn.timeout = .25
            head = self.srvConn.read(10);
            if (len(head) < 10 or not(head[0:5] == '##IMJ')):
                print time.asctime(), "no head read (%d)" % self.srvConn.inWaiting()
                self.srvConn.flushInput()
                self.srvConn.flushOutput()
                return

            frameHead = unpack('<ccccccHxx', head)

            print('after  %d %s' % (self.srvConn.inWaiting(), head[0:5]))

            # approximate number of seconds @ 14KB/s and pad by 30%
            self.srvConn.timeout = 1.25
                        
            #print "timeout: ", self.srvConn.timeout

            self.frame = self.srvConn.read(frameHead[6])

            print time.asctime(), ", read frame %d / %d" % (len(self.frame), frameHead[6])
        except Exception, inst:
            print 'Problem during frame capture', inst

    def is_connected(self):
        return self.connected
    def add_viewer(self, q):
        self.viewers.append(q)
    def get_jpeg(self):
        return self.frame
    def send_command(self, cmd, blocking=False):
        #self.commands.put(binascii.a2b_hex(cmd), False)
        c = SrvCommand(binascii.a2b_hex(cmd))
        q = Queue.Queue(1)
        if blocking:
            c.queue = q
        self.commands.put(c, False)
        if not blocking:
            return 'Scheduled command: ' + cmd
        else:
            return q.get()
