'''
Created on 4.3.2018

@author: Sami<sami@tabloiti.com>
'''

import pygame
import os
import select
import sys
import time
from time import sleep
import botutils
import emotiondraw as eye
from random import randint
import config
import weatherdraw as ws

if config.CAMEENABLED:
	import facedetect as face

from threading import Thread

this = sys.modules[__name__]

detect = False
global faceFound 
global fx, fy

this.faceFound = False
this.blinkCount = 0
this.fps = 0
this.BLINKMAX = 10
this.nextBlink = 0
this.blinkStart = 0
this.t = 0
this.detectStart = 0
this.showimg = False

#set default emotion for start
this.state = eye.NEUTRAL
this.oldState = state
this.gosleep = 0

#Aiqu modes, EYE, RADIO, WEATHER, SLEEP
this.mode  = 'EYE'


#
# ALL FUNCTIONS START HERE
#
def wakeup():
    this.gosleep = time.time()

def keyboard():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			stoped = True
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				state = eye.LOOKRIGHT
				eye.lookright(lcd)
			if event.key == pygame.K_LEFT:
				state =  eye.LOOKLEFT
				eye.lookleft(lcd)
			if event.key == pygame.K_UP:
				state = eye.NEUTRAL
				eye.neutral(lcd)
			if event.key == pygame.K_DOWN:
				state = eye.LOOKDOWN
				eye.lookdown(lcd)
			if event.key == pygame.K_d:
				state = eye.DOUBT
				eye.doubt(lcd)
			if event.key == pygame.K_h:
				state = eye.HAPPY
				eye.happy(lcd)
			if event.key == pygame.K_w:
				this.mode = "WEATHER"
#
# HANDLE EYE UPDATE IN LOOP				
def eyemode(lcd, myip, readTemp, clock):
	#BLINK ANIMATE

	dif =  time.time() - this.blinkStart
	
	#check if switch to sleeping mode, due no action ongoing
    	sleep = time.time() - this.gosleep
	#print "Sleep: ",sleep
	sleeping = False
	if sleep >= config.SLEEP:
	    #print "zzzz"
	    sleeping = True

	
	if sleeping:
	    this.oldState = this.state
	    eye.sleep(lcd)
	else:
		if dif >= this.nextBlink and this.blinkCount == 0 and this.state != eye.DOUBT:
			#print "blink start"
			this.oldState = this.state
			this.state = eye.BLINK
			eye.blink(lcd)
			this.blinkCount = this.blinkCount +1
		elif this.blinkCount == 1:
			#print "neutral"
			this.state = this.oldState
			#eye.neutral(lcd)
			this.blinkCount = this.blinkCount +1
		elif this.blinkCount == 2:
			#print "blink 2"
			this.state = eye.BLINK
			eye.blink(lcd)
			this.blinkStart = time.time()
			this.nextBlink = randint(1, BLINKMAX);
			this.blinkCount = 0
		else:
			#print "old state"
			this.state = this.oldState
			#eye.neutral(lcd)
			this.blinkCount = 0
		
		#BLINK ANIMATE DONE
		
		#EYE states
		if this.state == eye.NEUTRAL:
			eye.neutral(lcd)
		if this.state == eye.LOOKDOWN:
			eye.lookdown(lcd)
		if this.state == eye.LOOKRIGHT: 
			eye.lookright(lcd)
		if this.state == eye.LOOKLEFT:
			eye.lookleft(lcd)
		if this.state == eye.DOUBT:
			eye.doubt(lcd)
		if this.state == eye.HAPPY:
			eye.happy(lcd)
		if this.state == eye.BLINK:
			eye.blink(lcd)
	#Else normal mode end here
	
	## All bellowed are need in any mode
	this.fps = clock.get_fps()
	eye.texts(lcd,this.fps, myip, mode)

	#For test eye move via console input
	i,o,e = select.select([sys.stdin],[],[],0.0001)
	for s in i:
		if s == sys.stdin:
			input = sys.stdin.readline()
			wakeup()
			if input.startswith('r'):
				print "Right"
				this.state = eye.LOOKRIGHT
				eye.lookright(lcd)
			if input.startswith('l'):
				this.state =  eye.LOOKLEFT
				eye.lookleft(lcd)
			if input.startswith('n'):
				this.state = eye.NEUTRAL
				eye.neutral(lcd)
			if input.startswith('d'):
				this.state = eye.LOOKDOWN
				eye.lookdown(lcd)
			if input.startswith('y'):
				this.state = eye.DOUBT
				eye.doubt(lcd)
			if input.startswith('h'):
				this.state = eye.HAPPY
				eye.happy(lcd)
				
			if input.startswith('i'):
				if(this.showimg):
					this.showimg = False
				else:
					this.showimg = True
					
			if input.startswith('w'):
				print("Wearther mode")
				this.mode = "WEATHER"
				
			if input.startswith('fen'):
					if(fen):
						fen = False
					else:
					    fen = True
			if input.startswith('e'):
				print("Bye Bye!")
				raise SystemExit

			print "echo:" + input
			this.oldState = this.state
		 
			#keyboard()
				
			this.oldState = this.state
	dif =  time.time() - readTemp
	if dif >= 20:
		readTemp = time.time()
		global temp
		temp = botutils.cpu_temp() 
	if faceFound:
		eye.facedetect(lcd, temp + " FACE FOUND:")
	else:
		eye.facedetect(lcd, temp + "")

	if this.showimg:
		try:
			img=pygame.image.load("result.jpg") 
			#screen.blit(img,(0,0))
			lcd.blit(pygame.transform.scale(img, (100, 100)), (0, 20))
		except:
			print "FAIL LOAD IMG"

	clock.tick(60)
	pygame.display.update()

	if config.CAMEENABLED:
		if not this.t.isAlive():
			dif =  time.time() - this.detectStart 
			if dif >= 5:
				this.detectStart = time.time()
				if config.CAMEENABLED:
					this.t = face.DetectThread(detectCB)
					this.t.start()
# END EYE MODE HANDLE

	
#
#
# Callback for facedetect
#
def detectCB(result, x, y):
	if config.CAMEENABLED:
		print "Detect result: " + str(result)
		print "Face x:" + str(x) + " y:" + str(y)
		global faceFound
		global fx, fy
		fx = x
		fy = y
		faceFound = result
#	if result:
#		global faceFound
#		faceFound = True
#	else:
#		global faceFound
#		faceFound = False
	
#---------detecCB END -----------------------------------------------------------------------------

#Init detect thread
if config.CAMEENABLED:
	this.t = face.DetectThread(detectCB)

#--------------------------------------------------------------------------------------------------
#
# MAIN PROGRAM
#
#--------------------------------------------------------------------------------------------------
def main():
	print "Hit 'e' to exit! 'i' show face track image"
	stoped = False
	os.putenv('SDL_FBDEV', '/dev/fb1')
	this.showimg = False
	fen = False

	#Main code
	pygame.init()
	if config.ROTATE:
	    lcd = pygame.display.set_mode((320, 480),pygame.FULLSCREEN)
	else:
	    lcd = pygame.display.set_mode((480, 320),pygame.FULLSCREEN)
	#pygame.DOUBLEBUF)

	#initial values
	this.detectStart = time.time()
	readTemp = time.time()
	this.blinkStart = time.time()
	this.gosleep = time.time()
	clock = pygame.time.Clock()
	
	BLINKMAX = 10
        nextBlink = randint(1, BLINKMAX)


	#init eyes
	eye.neutral(lcd)
	myip = botutils.get_ip()

	pygame.display.update()
	pygame.mouse.set_visible(False)

	if config.CAMEENABLED:
		this.t = face.DetectThread(detectCB)
		this.t.start()

	global temp
	temp = botutils.cpu_temp()
	#MAIN LOOP START HERE
	#while not stoped:
	#while not stoped:
	while True:
		ev = pygame.event.poll()    # Look for any event
        	if ev.type == pygame.QUIT:  # Window close button clicked?
            		break                   #   ... leave game loop
			
		lcd.fill((0,0,0))
		
		if this.mode == "EYE":
			eyemode(lcd, myip, readTemp, clock)
		if this.mode == "WEATHER":
			ws.drawGUI(lcd)
			
	pygame.quit()     # Once we leave the loop, close the window.
#------------------END MAIN LOOPER-----------------------------------------------------------------
		
#Start botty		

main()	 

