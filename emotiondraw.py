'''
Emotion draw
Created on 4.3.2018

@author: Sami<sami@tabloiti.com>
'''
import roundrects
import pygame
from sys import getsizeof

RED = (255,0,0)
TUR = (50,156,198)
BLACK = (0,0,0)
WHITE = (255,255,255)

#SIZEW = 320
#SIZEH = 240
SIZEW = 480
SIZEH = 320

EW = 70*1.5
EH = 100*1.5
MARGIN = 10
EYPOS = (SIZEH/2)-(EH/2) #common for both eye
LEYPOS = (SIZEW/2)-(EW+MARGIN)
REYPOS = (SIZEW/2)+MARGIN 

#Emotions
NEUTRAL 	= 	1
LOOKDOWN 	= 	2
LOOKRIGHT 	= 	3
LOOKLEFT 	= 	4
DOUBT 		= 	5
HAPPY 		= 	6


def texts(surface, text1, text2):
   font=pygame.font.Font(None,20)
   font2 = pygame.font.Font(None,20)
   scoretext=font.render("FPS:" + str(text1), 1,WHITE)
   iptext = font2.render(text2, 1,WHITE)
   surface.blit(scoretext, (0, 0))
   surface.blit(iptext, (SIZEW-iptext.get_width()-5,SIZEH-iptext.get_height()-5))

def neutral(surface):
  #rect: (x1, y1, width, height)
  state = NEUTRAL
  #left
  roundrects.round_rect(surface, [LEYPOS, EYPOS+10, EW, EH-20], TUR, rad=30)
  #right
  roundrects.round_rect(surface, [REYPOS, EYPOS, EW, EH], TUR, rad=30)
  
def happy(surface):
  state = HAPPY
  #left
  roundrects.round_rect(surface, [LEYPOS, EYPOS, EW, EH], TUR, rad=30)
  #right
  roundrects.round_rect(surface, [REYPOS, EYPOS, EW, EH], TUR, rad=30)
  #draw blak box
  #rect: (x1, y1, width, height)
  pygame.draw.rect(surface, BLACK, [LEYPOS-10, EYPOS+20, (EW*2)+35, EH+15])


def doubt(surface):
  state = DOUBT
  points = list()

  points.append ( ((SIZEW/2)-5, SIZEH/2) ) #left bottom
  points.append (((SIZEW/2)+40, 0)) #top point
  points.append (((SIZEW/2)+150, (SIZEH/2)-50)) #oikealaita 290,100

  #left
  roundrects.round_rect(surface, [LEYPOS, EYPOS, EW, EH-20], TUR, rad=30)
  #right
  roundrects.round_rect(surface, [REYPOS, EYPOS, EW, EH-20], TUR, rad=30)

  pygame.draw.polygon(surface,BLACK, points)


def lookdown(surface):
  state = LOOKDOWN
  #left
  roundrects.round_rect(surface, [LEYPOS, EYPOS+20, EW, EH], TUR, rad=30)
  #right
  roundrects.round_rect(surface, [REYPOS, EYPOS+20, EW, EH], TUR, rad=30)


def lookright(surface):
  state = LOOKRIGHT
  roundrects.round_rect(surface, [LEYPOS+20, EYPOS, EW, EH-20], TUR, rad=30)
  #right
  roundrects.round_rect(surface, [REYPOS+20, EYPOS, EW, EH], TUR, rad=30)
  pygame.display.update()

def lookleft(surface):
  state = LOOKLEFT
  roundrects.round_rect(surface, [LEYPOS-20, EYPOS, EW, EH], TUR, rad=30)
  #right
  roundrects.round_rect(surface, [REYPOS-20, EYPOS, EW, EH-20], TUR, rad=30)

  