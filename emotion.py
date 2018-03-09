'''
Created on 4.3.2018

@author: Sami<sami@tabloiti.com>
'''


import pygame
import os
import select
import sys
from time import sleep
import botutils
import emotiondraw as eye

stoped = False

os.putenv('SDL_FBDEV', '/dev/fb1')

#set default emotion for start
state = eye.DOUBT

#Main code
pygame.init()
lcd = pygame.display.set_mode((480, 320),pygame.DOUBLEBUF)
#pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()
#init eyes
eye.doubt(lcd)
#get ip
myip = botutils.get_ip()

pygame.display.update()
pygame.mouse.set_visible(False)

fps = 0


#MAIN LOOP START HERE
while not stoped:
	lcd.fill((0,0,0))

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
			if input.startswith('e'):
				raise SystemExit

			print "echo:" + input
		 
		 
    #for test eye move from keybord
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

	clock.tick(25)
	pygame.display.update()
	#pygame.display.flip()
	

	 

