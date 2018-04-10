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
from espeak import espeak

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
this.clock = 0
this.readTemp = 0
this.sleeping = False

#Aiqu modes, EYE, RADIO, WEATHER, SLEEP, DEEP
this.mode  = 'EYE'


#
# ALL FUNCTIONS START HERE
#
def wakeup():
	print "WAKER UP!"
	this.state = eye.DOUBT
	this.mode = "EYE"
	this.sleeping = False
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
				state = eye.LOOKUP
				eye.lookup(lcd)
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
def eyemode(lcd, myip):
	
	#check if switch to sleeping mode, due no action ongoing
	sleep = time.time() - this.gosleep
	#print "Sleep: ",sleep
	
	this.sleeping = False
	if sleep >= config.SLEEP:
		this.sleeping = True

		#print "EYE STATE:" ,  this.state	

	if this.sleeping:
		this.oldState = this.state
		this.mode = "SLEEP"
		eye.sleep(lcd)
	else:
		#this.mode ="EYE"
		#BLINK ANIMATE
		
		dif =  time.time() - this.blinkStart
		
		if dif >= this.nextBlink and this.blinkCount == 0 and this.state != eye.DOUBT:
			print "blink start"
			this.oldState = this.state
			this.state = eye.BLINK
			eye.blink(lcd)
			this.blinkCount = this.blinkCount +1
		elif this.blinkCount == 1:
			print "neutral"
			this.state = this.oldState
			eye.neutral(lcd)
			this.blinkCount = this.blinkCount +1
		elif this.blinkCount == 2:
			print "blink 2"
			this.state = eye.BLINK
			eye.blink(lcd)
			this.blinkStart = time.time()
			print "Generate Rand"
			this.nextBlink = randint(1, BLINKMAX);
			this.blinkCount = 3
			print "NEXT"
		elif this.blinkCount == 3:
			print "back to normal"
			#this.state = this.oldState
			this.state = eye.NEUTRAL
			this.blinkCount = 0
		
		#BLINK ANIMATE DONE
		
		#EYE states
		if this.state == eye.NEUTRAL:
			eye.neutral(lcd)
		if this.state == eye.LOOKDOWN:
			eye.lookdown(lcd)
		if this.state == eye.LOOKUP:
			eye.lookup(lcd)
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
	
	pushUpdate(lcd, myip)
# END EYE MODE HANDLE

def pushUpdate(lcd, myip):
	
	## All bellowed are need in any mode
	this.clock.tick(40)
	this.fps = this.clock.get_fps()

	eye.texts(lcd,this.fps, myip, this.mode, this.state)
	#For test eye move via console input
	i,o,e = select.select([sys.stdin],[],[],0.0001)
	for s in i:
		if s == sys.stdin:
			input = sys.stdin.readline()
			if sleeping == True:
				wakeup()
			if input.startswith('r'):
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
			if	input.startswith('u'):
				this.state == eye.LOOKUP
				eye.lookup(lcd)
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
	dif =  time.time() - this.readTemp

	if dif >= 20:
		print "Read TEMP"
		this.readTemp = time.time()
		global temp
		temp = botutils.cpu_temp()
		
	if faceFound:
		eye.facedetect(lcd, temp + " FACE FOUND")
		if this.sleeping == True:
			print "CALL WAKEUP"
			wakeup()
	else:
		eye.facedetect(lcd, temp + "")

	if this.showimg == True:
		try:
			img=pygame.image.load("./temp/face.jpg") 
			#screen.blit(img,(0,0))
			img = pygame.transform.rotate(img,0)
			lcd.blit(pygame.transform.scale(img, (300, 300)), (0, 20))
		except:
			print "FAIL LOAD IMG"
	
	#print "UPDATE SCREEN ", this.fps
	pygame.display.update()
	
	
	if config.CAMEENABLED:
		if not this.t.isAlive():
			dif =  time.time() - this.detectStart 
			#print "DIF:" , dif
			if dif >= config.DETECT_DIF:
				this.detectStart = time.time()
				if config.CAMEENABLED:
					print "NEW DETECT THREAD"
					this.t = face.DetectThread(detectCB)
					this.t.setState(this.sleeping)
					this.t.start()

					
#
#
# Callback for facedetect
#
def detectCB(result, x, y, motion, pos):
	if config.CAMEENABLED:
		print "Detect result: " + str(result)
		print "Face x:" + str(x) + " y:" + str(y)
		global faceFound
		global fx, fy
		fx = x
		fy = y
		faceFound = result

		if motion and this.sleeping == True:
			#print "MOTION DETECTED " + pos
			print "MOTION WAKEUP"
			wakeup()
			
		if this.sleeping == False:
			if pos == "LEFT":
				print "Motion LEFT"
				this.state = eye.LOOKLEFT
			elif pos == "RIGHT":
				print "Motion Right"
				this.state = eye.LOOKRIGHT
			elif pos == "DOWN":
				print "Motion Down"
				this.state = eye.LOOKDOWN
			elif pos == "UP":
				print "Motion Up"
				this.state = eye.LOOKUP
			else:
				print "Motion Neutral"
				this.state = eye.NEUTRAL


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
	this.t.setState(this.sleeping)

#--------------------------------------------------------------------------------------------------
#
# MAIN PROGRAM
#
#--------------------------------------------------------------------------------------------------
def main():
	print "Hit 'e' to exit! 'i' show face track image"
	espeak.synth("Hello My name is AIQU")
	stoped = False
	os.putenv('SDL_FBDEV', config.OUTPUT)
	this.showimg = False
	fen = False

	#Main code
	pygame.init()
	if config.ROTATE:
        #320, 480
		lcd = pygame.display.set_mode((config.W, config.H), pygame.FULLSCREEN)
	else:
		lcd = pygame.display.set_mode((config.H, config.W), pygame.FULLSCREEN)
	#lcd = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
    #pygame.DOUBLEBUF)

	#initial values
	this.detectStart = time.time()
	this.readTemp = time.time()
	this.blinkStart = time.time()
	this.gosleep = time.time()
	this.clock = pygame.time.Clock()
	
	BLINKMAX = 10
	nextBlink = randint(1, BLINKMAX)


	#init eyes
	eye.neutral(lcd)
	myip = botutils.get_ip()

	pygame.display.update()
	pygame.mouse.set_visible(False)

	if config.CAMEENABLED:
		this.t = face.DetectThread(detectCB)
		this.t.setState(this.sleeping)
		this.t.start()

	global temp
	temp = botutils.cpu_temp()
	#MAIN LOOP START HERE
	#while not stoped:
	#this.clock.tick(config.fps)
	while True:
		#this.fps = this.clock.get_fps()
		#print "FPS:" , this.fps
		#print "LOOP start"
		
		ev = pygame.event.poll()    # Look for any event
		if ev.type == pygame.QUIT:  # Window close button clicked?
			break                   #   ... leave game loop
			
		lcd.fill((255,0,0))
		#print "LOOP midle: " ,sleeping
		#print this.mode
		
		if this.sleeping == True:
			eye.sleep(lcd)
			pushUpdate(lcd, myip)
		elif (this.mode == "EYE") or (this.mode == "SLEEP"):
			#print "NORMAL UPDATE"
			eyemode(lcd, myip)
		elif this.mode == "WEATHER":
			ws.drawGUI(lcd)
			pygame.display.update()
	print "LOOP end"
	pygame.quit()     # Once we leave the loop, close the window.
#------------------END MAIN LOOPER-----------------------------------------------------------------
		
#Start botty		

main()	 

