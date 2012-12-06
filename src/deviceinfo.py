#!/usr/bin/python
# Project Network - Logitech G27 / Xbox 360 controller and others

import os
import pygame  		# Imports pygame library that are made for developing games


pygame.init()			# Starts pygame
t = pygame.time.Clock()		# Make a tracker

os.system('cls' if os.name=='nt' else 'clear')# Clear terminal // remove "there is no soundcard"
try: 
	
	print "Number of Devices:", pygame.joystick.get_count()
	d = pygame.joystick.Joystick(0)
	d.init()			# Start pygame.joystick.Joystick(0)


# Gives info about the device
	print "Connected device", d.get_name()
	print d.get_name(), "have"
	print "Buttons:", d.get_numbuttons()
	print "Axes:", d.get_numaxes()
	print "Hats:", d.get_numhats()
	print "Balls:", d.get_numballs()
	print "The device ID is", d.get_id()
	print "Press button 0 to exit"

# Start showing the info in terminal
	def loop():
		global d, t
		while pygame.event.get(pygame.QUIT) == []:
			xy =pygame.event.get(pygame.JOYAXISMOTION) # call the infomation to
		# Axes Part
			if xy != []:
				xy_data = []
				for c in range(0, d.get_numaxes()):
					xy_data+= [str(round(d.get_axis(c),1))]
				print xy_data
			
			# Button Part Down
			downbutton = pygame.event.get(pygame.JOYBUTTONDOWN)
			for button in downbutton:
				print "Pressed button is", button.button
				if button.button == 0:			# The exit button
					return
		
		# Button Part Up
			upbutton = pygame.event.get(pygame.JOYBUTTONUP)
			for button in upbutton:
				print "Button released was", button.button
			t.tick(80)
	loop()

except:
	print "No device found"
	print "Please insert device and try agian" 
	print "Shutting down now"

#Nicklas Jensen


