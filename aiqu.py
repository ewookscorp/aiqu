'''
Created on 4.3.2018

@author: Sami<sami@tabloiti.com>
'''


#configuration
CAMEENABLED = False
#configureatio end


import pygame
import os
import select
import sys
import time
from time import sleep
import botutils
import emotiondraw as eye
from random import randint

if CAMEENABLED:
	import facedetect as face

from threading import Thread


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

detect = False
global faceFound 
global fx, fy
faceFound = False
#
# Callback for facedetect
#
def detectCB(result, x, y):
	if CAMEENABLED:
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
if CAMEENABLED:
	t = face.DetectThread(detectCB)

#--------------------------------------------------------------------------------------------------
#
# MAIN PROGRAM
#
#--------------------------------------------------------------------------------------------------
def main():
	print "Hit 'e' to exit! 'i' show face track image"
	stoped = False
	os.putenv('SDL_FBDEV', '/dev/fb1')
	showimg = False
	fen = False

	#set default emotion for start
	state = eye.NEUTRAL
	BLINKMAX = 10

	#Main code
	pygame.init()
	lcd = pygame.display.set_mode((480, 320),pygame.FULLSCREEN)
	#pygame.DOUBLEBUF)

	clock = pygame.time.Clock()
	blinkStart = time.time()
	detectStart = time.time()
	readTemp = time.time()	
	#init eyes
	eye.neutral(lcd)
	myip = botutils.get_ip()

	pygame.display.update()
	pygame.mouse.set_visible(False)

	fps = 0
	blinkCount = 0
	nextBlink = randint(1, BLINKMAX);
	oldState = state
	
	if CAMEENABLED:
		t = face.DetectThread(detectCB)
		t.start()

	global temp
	temp =botutils.cpu_temp()
	#MAIN LOOP START HERE
	#while not stoped:
	#while not stoped:
	while True:
		ev = pygame.event.poll()    # Look for any event
        	if ev.type == pygame.QUIT:  # Window close button clicked?
            		break                   #   ... leave game loop
			
		lcd.fill((0,0,0))
		
		#BLINK ANIMATE
		dif =  time.time() - blinkStart 
		#print dif
		#print nextBlink
		
		if dif >= nextBlink and blinkCount == 0 and state != eye.DOUBT:
			#print "blink"
			oldState = state
			state = eye.BLINK
			eye.blink(lcd)
			blinkCount = blinkCount +1
		elif blinkCount == 1:
			#print "neutral"
			state = oldState
			#eye.neutral(lcd)
			blinkCount = blinkCount +1
		elif blinkCount == 2:
			#print "blink2"
			state = eye.BLINK
			eye.blink(lcd)
			blinkStart = time.time()
			nextBlink = randint(1, BLINKMAX);
			blinkCount = 0
		else:
			#print "old state"
			state = oldState
			#eye.neutral(lcd)
			blinkCount = 0
			
		#BLINK ANIMATE DONE

		fps = clock.get_fps()
		eye.texts(lcd,fps, myip)
		
		#EYE states
		if state == eye.NEUTRAL:
			eye.neutral(lcd)
		if state == eye.LOOKDOWN:
			eye.lookdown(lcd)
		if state == eye.LOOKRIGHT: 
			eye.lookright(lcd)
		if state == eye.LOOKLEFT:
			eye.lookleft(lcd)
		if state == eye.DOUBT:
			eye.doubt(lcd)
		if state == eye.HAPPY:
			eye.happy(lcd)
		if state == eye.BLINK:
			eye.blink(lcd)

		#For test eye move via console input
		i,o,e = select.select([sys.stdin],[],[],0.0001)
		for s in i:
			if s == sys.stdin:
				input = sys.stdin.readline()

				if input.startswith('r'):
					print "Right"
					state = eye.LOOKRIGHT
					eye.lookright(lcd)
				if input.startswith('l'):
					state =  eye.LOOKLEFT
					eye.lookleft(lcd)
				if input.startswith('n'):
					state = eye.NEUTRAL
					eye.neutral(lcd)
				if input.startswith('d'):
					state = eye.LOOKDOWN
					eye.lookdown(lcd)
				if input.startswith('y'):
					state = eye.DOUBT
					eye.doubt(lcd)
				if input.startswith('h'):
					state = eye.HAPPY
					eye.happy(lcd)
				if input.startswith('i'):
					if(showimg):
						showimg = False
					else:
						showimg = True
				if input.startswith('fen'):
                                        if(fen):
                                                fen = False
                                        else:
                                                fen = True
				if input.startswith('e'):
					raise SystemExit

				print "echo:" + input
				oldState = state
			 
				#keyboard()
					
				oldState = state
		dif =  time.time() - readTemp
                if dif >= 20:
			readTemp = time.time()
			global temp
			temp =botutils.cpu_temp() 
		if faceFound:
			eye.facedetect(lcd, temp + " FACE FOUND:")
		else:
			eye.facedetect(lcd, temp + "")

		if showimg:
			try:
				img=pygame.image.load("result.jpg") 
				#screen.blit(img,(0,0))
				lcd.blit(pygame.transform.scale(img, (100, 100)), (0, 20))
			except:
				print "FAIL LOAD IMG"
		clock.tick(60)
		pygame.display.update()
		
		#if t.isAlive():
		#	t.join()
		#elif not t.isAlive():
		
		if CAMEENABLED:
			if not t.isAlive():
				dif =  time.time() - detectStart 
				if dif >= 5:
					detectStart = time.time()
					if CAMEENABLED:
						t = face.DetectThread(detectCB)
						t.start()
		
		#if not fen:
		#	if t.isAlive():
		#		print "Force kill"
		#		t.join()
		#	eye.facedetect(lcd, "-")
			
	pygame.quit()     # Once we leave the loop, close the window.
#------------------END MAIN LOOPER-----------------------------------------------------------------
		
#Start botty		

main()	 

