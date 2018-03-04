'''
Created on 4.3.2018

@author: Sami<sami@tabloiti.com>
'''
import pygame
import os
import roundrects
from time import sleep

RED = (255,0,0)
TUR = (50,156,198)

SIZEW = 320
SIZEH = 240

EW = 70*1.5
EH = 100*1.5
EPOS = 40
LEYPOS = 50
REYPOS = 160

stoped = False

os.putenv('SDL_FBDEV', '/dev/fb1')
state = 1


def texts(score):
   lcd.fill((0,0,0))
   font=pygame.font.Font(None,30)
   scoretext=font.render("FPS:" + str(score), 1,(255,255,255))
   lcd.blit(scoretext, (0, 0))
   #pygame.display.update()

def neutral():
  state = 1
  #lcd.fill((0,0,0))
  #left eye
  pygame.draw.ellipse(lcd, TUR, [LEYPOS, EPOS, EW, EH])
  #right eye
  pygame.draw.ellipse(lcd, TUR, [REYPOS, EPOS, EW, EH])
  pygame.display.update()

def lookdown():
  state = 2
  #lcd.fill((0,0,0))
  #left eye
  pygame.draw.ellipse(lcd, TUR, [LEYPOS, EPOS+20, EW, EH])
  #right eye
  pygame.draw.ellipse(lcd, TUR, [REYPOS, EPOS+20, EW, EH])
  pygame.display.update()


def lookright():
  state = 3
  #lcd.fill((0,0,0))
  #left eye
  pygame.draw.ellipse(lcd, TUR, [LEYPOS+20, EPOS, EW, EH])
  #right eye
  pygame.draw.ellipse(lcd, TUR, [REYPOS+20, EPOS, EW, EH])
  pygame.display.update()

def lookleft():
  state = 4
  #lcd.fill((0,0,0))
  #left eye
  pygame.draw.ellipse(lcd, TUR, [LEYPOS-20, EPOS, EW, EH])
  #right eye
  pygame.draw.ellipse(lcd, TUR, [REYPOS-20, EPOS, EW, EH])
  pygame.display.update()
  

#Main code
pygame.init()
lcd = pygame.display.set_mode((320, 240))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

#lcd.fill((255,0,0))
#pic = pygame.image.load("Star.png")
#picPosit = (10, 10)
#lcd.blit(pic, picPosit)

neutral()
#pygame.display.set_caption('A bit Racey')

pygame.display.update()
#sleep(10)
pygame.mouse.set_visible(False)

#lcd.fill((0,0,0))
#pygame.display.update()
#sleep(10)

fps = 0

while not stoped:
 fps = fps+1
 if fps >= 60:
	fps = 0;

 texts(fps)
 if state == 1:
	neutral()
 if state == 2:
	lookdown()
 if state == 3: 
	lookright()
 if state == 4:
	lookleft()
 #sleep(2)
 pygame.display.update()
 clock.tick(60)

 for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stoped = True

	if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_RIGHT:
		state = 3
    	   	lookright()
	   if event.key == pygame.K_LEFT:
		state = 4
                lookleft()
	   if event.key == pygame.K_UP:
		state = 1
                neutral()
	   if event.key == pygame.K_DOWN:
		state = 2
                lookdown()
	 

