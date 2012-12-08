'''
Created on 8 Dec 2012

@author: moz

Inspiration:
- https://github.com/NJensen/TT_DeviceInfo.py
'''
import pygame.joystick
import sys
import threading

class JoystickController(object):
    '''
    classdocs
    '''
    _Robot = None
    _ContinueLoop = threading.Event()
    _QuitButton = 9
    
    def __init__(self, Robot, DeviceNo = 0 ):
        '''
        Constructor
        '''
        pygame.init()            # Starts pygame

        print >> sys.stderr, "Number of Devices:", pygame.joystick.get_count()
        if not pygame.joystick.get_count() > 0:
            raise IOError( "No joystick devices available")
            
        self._joystick = pygame.joystick.Joystick(DeviceNo)
        self._joystick.init()            # Start pygame.joystick.Joystick(0)

        self._Robot = Robot
        self.Enable()


    def Enable(self):
        ''' Loop control, starts the acquisition and command loop '''
        self._ContinueLoop.set()
        self._SrvThread = threading.Thread(target=self._loop, name="JoystickController")
        self._SrvThread.start()

    def Disable(self):
        ''' Loop control, ends the acquisition and command loop '''
        pygame.event.post( pygame.event.Event(pygame.QUIT ) )
        self._ContinueLoop.clear()        

    def _loop(self):
        print >> sys.stderr, "Joystick main loop started"
        while self._ContinueLoop.isSet():
#        while True:
            Ev = pygame.event.wait()    # wait for any event to happen and return the first one

            # quit event by pygame.
            if Ev.type == pygame.QUIT:
                print >> sys.stderr, "Pygame guit event. Setitng direciton neutral and quitting"
                self._Robot.SetDirection( [0, 0] )
                self._ContinueLoop.clear()
                continue

            # Axes Part
            if Ev.type == pygame.JOYAXISMOTION:
                xy_data = []
                for c in range(0, self._joystick.get_numaxes()):
                    xy_data += [ round(self._joystick.get_axis(c),1)]

                print >> sys.stderr, "Setting direction: %s"%xy_data                
                self._Robot.SetDirection( xy_data )
                continue
                           
            # Button Part Down
            if Ev.type == pygame.JOYBUTTONDOWN:
                if Ev.button == self._QuitButton:            # The exit button
                    print >> sys.stderr, "Button %d is exit button."%(self._QuitButton+1)
                    self.Disable()
                    continue
                    
#        
#            # Button Part Up
#            upbutton = pygame.event.get(pygame.JOYBUTTONUP)
#            for button in upbutton:
#                print "Button released was", button.button
            
#            t.tick(80)
        print >> sys.stderr, "Joystick main loop ended"
