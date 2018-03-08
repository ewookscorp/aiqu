'''
Created on 4.3.2018

@author: Sami<sami@tabloiti.com>
'''
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
import os
import socket
import roundrects
import select
import sys
from time import sleep

RED = (255,0,0)
TUR = (50,156,198)
BLACK = (0,0,0)

SIZEW = 320
SIZEH = 240

EW = 70*1.5
EH = 100*1.5
EPOS = 40
LEYPOS = 50
REYPOS = 160

stoped = False

os.putenv('SDL_FBDEV', '/dev/fb1')

#Emotions
NEUTRAL 	= 	1
LOOKDOWN 	= 	2
LOOKRIGHT 	= 	3
LOOKLEFT 	= 	4
DOUBT 		= 	5
HAPPY 		= 	6

#set default emotion for start
state = DOUBT


def texts(score):
   lcd.fill((0,0,0))
   font=pygame.font.Font(None,30)
   font2 = pygame.font.Font(None,20)
   scoretext=font.render("FPS:" + str(score), 1,(255,255,255))
   iptext = font2.render(myip, 1,(255,255,255))
   lcd.blit(scoretext, (0, 0))
   lcd.blit(iptext, (210,220))

def neutral():
  state = NEUTRAL
  #left eye
  #pygame.draw.ellipse(lcd, TUR, [LEYPOS, EPOS, EW, EH-10])
  #right eye
  #pygame.draw.ellipse(lcd, TUR, [REYPOS, EPOS, EW, EH])
  #pygame.draw.polygon(lcd,RED, points)
  #left
  roundrects.round_rect(lcd, [LEYPOS, EPOS+10, EW, EH-20], TUR, rad=30)
  #right
  roundrects.round_rect(lcd, [REYPOS, EPOS, EW, EH], TUR, rad=30)
  #pygame.display.update()

def happy():
  state = HAPPY
  #left eye
  #pygame.draw.ellipse(lcd, TUR, [LEYPOS, EPOS, EW, EH])
  #right eye
  #pygame.draw.ellipse(lcd, TUR, [REYPOS, EPOS, EW, EH])

  #left
  roundrects.round_rect(lcd, [LEYPOS, EPOS, EW, EH], TUR, rad=30)
  #right
  roundrects.round_rect(lcd, [REYPOS, EPOS, EW, EH], TUR, rad=30)

  #draw blak box
  pygame.draw.rect(lcd, BLACK, [50, 80, 250, 130])
  #pygame.display.update()

def doubt():
  state = DOUBT
  points = list()
  points.append ((165,0)) #top 185,0
  points.append ((200,0)) #top 185,0
  points.append ((300,85)) #oikealaita 290,100
  points.append ((200,115)) #alareuna keski 200,120
  points.append ((155,130)) #vasen 152,130

  #left
  roundrects.round_rect(lcd, [LEYPOS, EPOS, EW, EH-20], TUR, rad=30)
  #right
  roundrects.round_rect(lcd, [REYPOS, EPOS, EW, EH-20], TUR, rad=30)

  pygame.draw.polygon(lcd,BLACK, points)
  #pygame.display.update()


def lookdown():
  state = LOOKDOWN
  #left eye
  #pygame.draw.ellipse(lcd, TUR, [LEYPOS, EPOS+20, EW, EH])
  #right eye
  #pygame.draw.ellipse(lcd, TUR, [REYPOS, EPOS+20, EW, EH])
  
  #left
  roundrects.round_rect(lcd, [LEYPOS, EPOS+20, EW, EH], TUR, rad=30)
  #right
  roundrects.round_rect(lcd, [REYPOS, EPOS+20, EW, EH], TUR, rad=30)

  #pygame.display.update()


def lookright():
  state = LOOKRIGHT
  #left eye
  #pygame.draw.ellipse(lcd, TUR, [LEYPOS+20, EPOS, EW, EH])
  #right eye
  #pygame.draw.ellipse(lcd, TUR, [REYPOS+20, EPOS, EW, EH])
  #left
  roundrects.round_rect(lcd, [LEYPOS+20, EPOS, EW, EH-20], TUR, rad=30)
  #right
  roundrects.round_rect(lcd, [REYPOS+20, EPOS, EW, EH], TUR, rad=30)
  pygame.display.update()

def lookleft():
  state = LOOKLEFT
  #left eye
  #pygame.draw.ellipse(lcd, TUR, [LEYPOS-20, EPOS, EW, EH])
  #right eye
  #pygame.draw.ellipse(lcd, TUR, [REYPOS-20, EPOS, EW, EH])
  #left
  roundrects.round_rect(lcd, [LEYPOS-20, EPOS, EW, EH], TUR, rad=30)
  #right
  roundrects.round_rect(lcd, [REYPOS-20, EPOS, EW, EH-20], TUR, rad=30)

  #pygame.display.update()
  

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

#Main code
pygame.init()
#pygame.HWSURFACE
#pygame.DOUBLEBUF
lcd = pygame.display.set_mode((480, 320),pygame.OPENGL|pygame.DOUBLEBUF)
#pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()

#points = list()
#points.append ((185,0)) #top
#points.append ((290,100)) #oikealaita
#points.append ((200,120)) #alareuna keski
#points.append ((152,130)) #vasen

#neutral()
doubt()

#get ip
myip = get_ip()

pygame.display.update()
pygame.mouse.set_visible(False)

fps = 0


#MAIN LOOP START HERE
while not stoped:
 #fps = fps+1
 #if fps >= 60:
 #	fps = 0;
 fps = clock.get_fps()
 texts(fps)
 print fps
 if state == NEUTRAL:
	neutral()
 if state == LOOKDOWN:
	lookdown()
 if state == LOOKRIGHT: 
	lookright()
 if state == LOOKLEFT:
	lookleft()
 if state == DOUBT:
	doubt()
 if state == HAPPY:
	happy()

 #sleep(2)
 pygame.display.update()
 #pygame.display.flip()
 clock.tick(25)
 i,o,e = select.select([sys.stdin],[],[],0.0001)
 for s in i:
 	if s == sys.stdin:
 		input = sys.stdin.readline()

		if input.startswith('r'):
			print "Right"
                	state = LOOKRIGHT
                	lookright()
           	if input.startswith('l'):
                	state =  LOOKLEFT
                	lookleft()
           	if input.startswith('n'):
                	state = NEUTRAL
                	neutral()
           	if input.startswith('d'):
                	state = LOOKDOWN
                	lookdown()
           	if input.startswith('y'):
                	state = DOUBT
                	doubt()
           	if input.startswith('h'):
                	state = HAPPY
                	happy()
		if input.startswith('e'):
			raise SystemExit

		print "echo:" + input
		 
 
 for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stoped = True

	if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_RIGHT:
		state = LOOKRIGHT
    	   	lookright()
	   if event.key == pygame.K_LEFT:
		state =  LOOKLEFT
                lookleft()
	   if event.key == pygame.K_UP:
		state = NEUTRAL
                neutral()
	   if event.key == pygame.K_DOWN:
		state = LOOKDOWN
                lookdown()
	   if event.key == pygame.K_d:
		state = DOUBT
		doubt()
	   if event.key == pygame.K_h:
                state = HAPPY
                happy()

	 

