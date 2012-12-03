# pySRV1Console.py - base station console for SRV-1 robot
# Copyright (C) 2006-2007 Surveyor Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details (www.gnu.org/licenses)

#import Image, ImageDraw, StringIO, random

#from threading import Thread
import SocketServer, SimpleHTTPServer, BaseHTTPServer, cgi #, httplib
import Queue, time, select, os, stat, binascii, sys
#from struct import *
from string import atoi #, find
from SRVcom import Srv1

#import serial

HOST_NAME = ''
PORT_NUMBER = 8888
CONNECT_ON_STARTUP = True
SCAN_ENABLED = False
MAX_LOG_MESSAGES = 50  # Max log lines to keep
COM_PORT = '/tmp/serial'

class SizedDict(dict):
    def __init__(self, size=1000):
        dict.__init__(self)
        self._maxsize = size
        self._stack = []

    def __setitem__(self, name, value):
        if len(self._stack) >= self._maxsize:
            self.__delitem__(self._stack[0])
            del self._stack[0]
        self._stack.append(name)
        return dict.__setitem__(self, name, value)

log_messages = SizedDict(MAX_LOG_MESSAGES)
def log(message, console=False):
    if len(message) > 100:
        log_messages[time.time()] = message[0:100] + '...'
    else:
        log_messages[time.time()] = message
    if console:
        print time.asctime(), message



class Srv1HttpRequestHandler (SimpleHTTPServer.SimpleHTTPRequestHandler):
    server_version = 'Srv1Server/1.0'
    def do_GET (self):
        try:
            # default response
            response = "<html>SRV-1 Server (%s)</html>" % self.path
            ct = "text/html"
            resource = self.path.split('?',1)[0]

            if resource == "/srv_frame.jpg":
                if not self.server.srv1.is_connected():
                    self.send_redirect('media/loading.gif')
                    return
                else:
                    ct = "image/jpeg"
                    response = self.server.srv1.get_jpeg()
            elif resource == "/srv_stream.jpg":
                if not self.server.srv1.is_connected():
                    self.send_redirect('media/loading.gif')
                    return
                else:
                    self.srv_stream()
            elif resource == "/srv_log":
                response = self.srv_log()
            elif resource == "/srv_command":
                response = self.srv_command()
            elif resource == "/srv_fw_update":
                self.srv_fw_update()
                return
            else:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
                return

            self.send_response(200)
            self.send_header("Content-type", ct)
            self.end_headers()
            self.wfile.write(response)
        except Exception, e:
            print e

    def send_redirect(self, loc):
        self.send_response(302)
        #self.send_header("Content-type", "text/html")
        self.send_header("Location", loc)
        self.end_headers()
        #self.wfile.write('<META HTTP-EQUIV="refresh" CONTENT="0;URL=%s">' % loc)

    def get_req_param(self, param):
        # lazy parsing of query string
        if not hasattr(self, 'params'):
            self.params = {}
            if self.path.find('?')>-1:
                self.params = cgi.parse_qs(self.path.split('?',1)[1], keep_blank_values=1)
        if self.params.has_key(param):
            return self.params[param][0]
        else:
            return ''

    # send MJPEG stream
    def srv_stream(self):
        self.send_response(200)
        #self.send_header("Content-type", "multipart/x-mixed-replace; boundary=ServerPush")
        self.send_header("Content-type", "multipart/x-mixed-replace;boundary=myboundary")
        self.end_headers()
        q = Queue.Queue(1)  # frame queue that we'll pass to the SRV1 object
        self.server.srv1.add_viewer(q)
        while True:
            f = q.get().strip()
            #self.wfile.write("--myboundary\r\nContent-type: image/jpeg\r\n\r\n")
            self.wfile.write("--myboundary\nContent-type: image/jpeg\nContent-Length: %d\n\n" % len(f))
            self.wfile.write(f)
            self.wfile.write("\n\n")
            self.wfile.flush()

    # update SRV-1 firmware by invoking the lpc21isp command line tool
    def srv_fw_update(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.get_req_param('confirm') == 'true':
            self.server.srv1.disconnect()
            self.wfile.write('<pre style="font-family: courier, serif; font-size: 12px;">')
            cmd_line = 'lpc21isp -hex srv1.hex %s 115200 14746' % self.server.srv1.comPort
            self.wfile.write(cmd_line + '\r\n')
            c = os.popen(cmd_line)
            l = c.read(8)
            while l:
                self.wfile.write(l)
                self.wfile.flush()
                l = c.read(8)
            self.wfile.write('</pre>')
        else:
            fw_stat = os.stat('srv1.hex');
            response = '<div style="font-family: arial, helvetica, sans-serif; font-size: 12px;">Preparing to load firmware (<i>srv1.hex</i>)...<br><br>File Size: %d<br/>Last Modified: %s<br><br>Installed Version: %s' % (fw_stat[stat.ST_SIZE], time.ctime(fw_stat[stat.ST_MTIME]), self.server.srv1.fw_version)
            response += '<br><br><form action="/srv_fw_update" method="GET"><input type="hidden" name="confirm" value="true"/><input type="submit" value="Continue" /></form></div>'
            self.wfile.write(response)

    # format and print log messages
    def srv_log(self):
        log = []
        log_times = log_messages.keys()
        log_times.sort(reverse=True)
        for k in log_times:
            log.append('<b>')
            log.append(time.asctime(time.localtime(k)))
            log.append(': </b>')
            log.append(log_messages[k])
            log.append('<br>')
        return ''.join(log)

    # enqueue a command
    def srv_command(self):
        blocking = False
        cmd = self.get_req_param('cmd')

        if 'ascii' == self.get_req_param('fmt'):
            cmd =  binascii.b2a_hex(cmd)
        if 'true' == self.get_req_param('blocking'):
            blocking = True

        #print '^^^', self.get_req_param('fmt'), blocking, cmd

        if cmd == 'connect':
            self.server.srv1.connect()
            return 'connect'
        elif cmd == 'disconnect':
            self.server.srv1.disconnect()
            return 'disconnect'
        else:
            return self.server.srv1.send_command(cmd, blocking)


# Uncomment these lines to disable stdout request logging 
#    def log_message(self, format, *args):
#        return

class Srv1HttpServer (SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): 
    
    def serve_forever (self):
        self.srv1 = Srv1(COM_PORT, CONNECT_ON_STARTUP)
        self.srv1.setDaemon(True)
        self.srv1.start()
        self.stop = False
        while not self.stop:
            r,w,e = select.select([self.socket], [], [], 1) # @UnusedVariable
            if r:
                self.handle_request()
        self.srv1.disconnect()

if __name__ == '__main__':

    for i in range(len(sys.argv)):
        if '-c' == sys.argv[i].lower():
            CONNECT_ON_STARTUP = True
        elif '-s' == sys.argv[i].lower():
            SCAN_ENABLED = True
        elif '-p' == sys.argv[i].lower():
            PORT_NUMBER = atoi(sys.argv[i + 1])
        elif '-com' == sys.argv[i].lower():
            COM_PORT = sys.argv[i + 1]

    log("SRV-1 Console Startup - %s" % (PORT_NUMBER), True)

    server_address = (HOST_NAME, PORT_NUMBER)
    httpd = Srv1HttpServer(server_address, Srv1HttpRequestHandler)
    httpd.daemon_threads = True

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    log("SRV-1 Console Stopped - %s" % (PORT_NUMBER), True)
