'''
Created on 5.4.2018
AIQU - project
@author: Sami<sami@tabloiti.com>
'''

from pprint import pprint
import requests
import config
import pygame

RED = (255,0,0)
TUR = (50,156,198)
BLACK = (0,0,0)
WHITE = (255,255,255)

if config.ROTATE:
    SIZEW = 320
    SIZEH = 480
else:
    SIZEW = 480
    SIZEH = 320


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

def texts(surface, text1, text2):
   font=pygame.font.Font(None,20)
   font2 = pygame.font.Font(None,20)
   scoretext=font.render("FPS:" + str(text1), 1,WHITE)
   iptext = font2.render(text2, 1,WHITE)
   surface.blit(scoretext, (0, 0))
   surface.blit(iptext, (SIZEW-iptext.get_width()-5,SIZEH-iptext.get_height()-5))



def drawGUI(surface):
    bg = pygame.image.load("wet.png")
    #BackGround = Background('wet.png', [0,0])
    surface.fill([255, 255, 255])
    surface.blit(bg, [0,0])
    texts(surface, "Testi", "Testi")
    print "Draw bg"

#getWeather()
