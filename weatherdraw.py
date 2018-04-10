'''
Created on 5.4.2018
AIQU - project
@author: Sami<sami@tabloiti.com>
'''

from pprint import pprint
import requests
import config
import pygame
import sys
from time import gmtime, strftime

RED = (255,0,0)
TUR = (50,156,198)
BLACK = (0,0,0)
BLACKT =(0,0,0,127)
WHITE = (255,255,255)
LGRAY = (192,192,192)
LGRAY2 = (119,136,153)

if config.ROTATE:
    SIZEW = config.H
    SIZEH = config.W
else:
    SIZEW = config.W
    SIZEH = config.H

this = sys.modules[__name__]
this.bg=pygame.image.load("wet.jpg")

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

#
# get current location weather json and save it to disk
#
def getWeather():
     r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + config.city  + '&APPID=' + config.apikey)
     pprint(r.json())
     return r


def texts(surface, text1, text2):
   font=pygame.font.Font(None,20)
   font2 = pygame.font.Font("fonts/Oswald-Light.ttf",20)
   font3 = pygame.font.Font("fonts/Oswald-Heavy.ttf",70)
   #get current clock
   ctime = strftime("%H:%M:%S", gmtime())
   cdate = strftime("%A %d %B", gmtime())
   time = font3.render(ctime, 1,BLACK)
   date = font2.render(cdate, 1,BLACK)
   scoretext=font.render("FPS:" + str(text1), 1,WHITE)
   iptext = font2.render(text2, 1,WHITE)
   surface.blit(time, (SIZEW/2-time.get_width()/2, 10))
   surface.blit(date, (SIZEW/2-date.get_width()/2, time.get_height()+2))
   surface.blit(scoretext, (0, 0))
   surface.blit(iptext, (SIZEW-iptext.get_width()-5,SIZEH-iptext.get_height()-5))


def drawGUI(surface):
    BackGround = Background('wet_up.jpg', [0,0])
    #surface.set_alpha(128) 
    surface.fill([255, 255, 255])
    surface.blit(BackGround.image, BackGround.rect)
    pygame.draw.rect(surface, BLACKT, (25,SIZEH/2.5,SIZEW-50,SIZEH/2-10))
    texts(surface, "Testi", "Testi")

#getWeather()
