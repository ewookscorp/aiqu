#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals


import pi3d
import os
import math
import random
from random import randint
import thread
import time
from svg.path import Path, parse_path
from xml.dom.minidom import parse
from gfxutil import *
import config
import sys
import emotionstates as eye
from multiprocessing.connection import Listener
import select
import sys
from multiprocessing.connection import Listener
import json
import logging
import speak

'''if config.CAMEENABLED:
    import camerathread
    #import facedetect as face
'''
logging.basicConfig(filename='aiqubase.log', level=logging.DEBUG)
sys.path.insert(1, '/home/pi/aiqu')
os.putenv('SDL_FBDEV', '/dev/fb1')
#this = sys.modules[__name__]


DISPLAY = pi3d.Display.create()
DISPLAY.set_background(0, 0, 0, 1)


light  = pi3d.Light(lightpos=(0, -500, -500), lightamb=(0.2, 0.2, 0.2))


global sleeping
global mode
global state
global oldState
global mode
global canvas

#Variables are defined here
#Aiqu modes, EYE, RADIO, WEATHER, SLEEP, DEEP
mode = "EYE"

#sleepTimer = 0
sleeping = False

state = eye.NEUTRAL
oldState = state

detectTimer = 0

LOGGER = pi3d.Log(level='DEBUG', file='aiqu.log')

def wakeup():
    LOGGER.info('WAKE UP!')
    state = eye.NEUTRAL
    mode = "EYE"
    sleeping = False
    sleepTimer = time.time()


def tex_load(DISPLAY, fname):
  ''' return a slide object'''
  slide = Slide()
  if not os.path.isfile(fname):
    return None
  tex = pi3d.Texture(fname, blend=True, mipmap=config.MIPMAP, m_repeat=True)
  xrat = DISPLAY.width/tex.ix
  yrat = DISPLAY.height/tex.iy
  if yrat < xrat:
    xrat = yrat
  wi, hi = tex.ix * xrat, tex.iy * xrat
  xi = (DISPLAY.width - wi)/2
  yi = (DISPLAY.height - hi)/2
  slide.tex = tex
  slide.dimensions = (wi, hi, xi, yi)
  return slide
  

def writeIPC(message, file):
    try:
        #FOR IPC Process
        pipe_name = file
        pipeout= open(pipe_name, 'w')
        pipeout.write(message)
        pipeout.close()
    except ValueError:
         LOGGER.info('Write ERR %s', ValueError) 
  
class Slide(object):
  def __init__(self):
    self.tex = None
    self.dimensions = None    
# Callback for facedetect
#
def detectCB(result, x, y, motion, pos):
    LOGGER.info('DETECT %s', motion)
    LOGGER.info('FACEFOUND %s', result)
    if config.CAMEENABLED:
        global faceFound
        global fx, fy
        fx = x
        fy = y
        faceFound = result

        if motion and sleeping == True:
            wakeup()
            
        if sleeping == False:
            if pos == "LEFT":
                state = eye.LOOKLEFT
            elif pos == "RIGHT":
                state = eye.LOOKRIGHT
            elif pos == "DOWN":
                state = eye.LOOKDOWN
            elif pos == "UP":
                state = eye.LOOKUP
            else:
                state = eye.NEUTRAL

##############END detect callback ##################################

class Eye:
    def __init__(self, sleep, blink):
        #Create canvas
        shader = pi3d.Shader("2d_flat")
        self.canvas = pi3d.Canvas()
        self.canvas.set_shader(shader)
        self.sleepTimer = sleep
        self.blinkTimer = blink
        self.sleeping = False
        self.blinkCount = 0

    def setTimers(self, sleep, blink):
        self.sleepTimer = sleep
        self.blinkTimer = blink
        #eye.draw(sbg, sfg, blink_img, neutral_img, sleeping)
        
    def draw(self, sbg, sfg, sleep):
        LOGGER.info('Start eye')
       
        self.canvas.set_draw_details(self.canvas.shader,[sfg.tex, sbg.tex]) # reset two textures
        self.canvas.set_2d_size(sbg.dimensions[0], sbg.dimensions[1], sbg.dimensions[2], sbg.dimensions[3])
        self.canvas.unif[48:54] = self.canvas.unif[42:48] #need to pass shader dimensions for both textures
        self.canvas.set_2d_size(sfg.dimensions[0], sfg.dimensions[1], sfg.dimensions[2], sfg.dimensions[3])
        self.canvas.draw()
        

####################### FUNCTIONS DEFINES END#######################################
try:
    LOGGER.info('START MAIN') 
    sleeping = False
    blinkCount = 0
    BLINKMAX = 10
    speak = speak.Speak()
    # eyeRadius is the size, in pixels, at which the whole eye will be rendered.
    if DISPLAY.width <= (DISPLAY.height * 2):
        # For WorldEye, eye size is -almost- full screen height
        eyeRadius   = DISPLAY.height / 2.1
    else:
        eyeRadius   = DISPLAY.height * 2 / 5


        
    #initialize timers
    blinkTimer = time.time()
    sleepTimer = time.time()
    nextBlink = randint(1, BLINKMAX)
    eyeDraw = Eye(sleepTimer, blinkTimer)


    # Load textures
    neutral = tex_load(DISPLAY, "textures/eyes/neutral.png")
    blink = tex_load(DISPLAY, "textures/eyes/blink.png")
    patimg = tex_load(DISPLAY, "textures/PATRN.PNG")
    coffimg = tex_load(DISPLAY, "textures/COFFEE.PNG")  

    sbg = neutral #tex_load("textures/eyes/neutral.png")
    sfg = sbg

    LOGGER.info('START MAIN loop')

    mykeys = pi3d.Keyboard()

    while DISPLAY.loop_running():
        #FOR IPC Process
        pipe_name = '/tmp/aigupipe'
        pipein = open(pipe_name, 'r')
        line = pipein.readline() #[:-1]
        LOGGER.info('PIPE Parent %d got "%s" at %s' % (os.getpid(), line, time.time( )))
        
        try:
            dataJson = None
            if not line:
                print('FILE IS EMPTY')
            else:
                dataJson = json.loads(line)
                
            pipein.close()
            LOGGER.info("JSON: %s", json.dumps(dataJson))
            if '{}' in json.dumps(dataJson):
                LOGGER.info("SKIP JSON")
            elif sleeping:
                LOGGER.info("JSON MOT: %s" ,dataJson['motion'])
                if dataJson['motion'] == True:
                    LOGGER.info("WAKE UP!!")
                    
                    if sleeping: 
                        writeIPC("0000:SLEEP", "/tmp/aiqumotionpipe")
                    sleeping = False
                    sbg = neutral
                    state = eye.NEUTRAL
                    mode = "EYE"
                    sleepTimer = time.time()
                    speak.speak("Hi!")
                    
        except:
            LOGGER.info("JSON ERROR")
            
        if (mode == "EYE") or (mode == "SLEEP"):
            LOGGER.info('waiting...')
            sleep = time.time() - sleepTimer
            LOGGER.info('waiting...2 %d', sleep)
            
            if sleep >= config.SLEEP:
                LOGGER.info('SLEEPING....')
                time.sleep(0.5)
                #wirte once
                if sleeping == False:
                    writeIPC("1:SLEEP", "/tmp/aiqumotionpipe")
                sleeping = True
                oldState = state
                mode = "SLEEP"
                sbg = blink
                
            
            if not sleeping:
               
                time.sleep(0.5)
                #Check if blink
                dif =  time.time() - blinkTimer
                LOGGER.info('Blink... %d', dif)
                LOGGER.info('Nextblink... %d', nextBlink)
                
                if dif >= nextBlink and blinkCount == 0:
                    LOGGER.info('Blink...')
                    oldState = state
                    state = eye.BLINK
                    sbg = blink
                    blinkCount = blinkCount +1
                    time.sleep(0.1)
                elif blinkCount == 1:
                    state = oldState
                    sbg = neutral
                    blinkCount = blinkCount +1
                    time.sleep(0.1)
                elif blinkCount == 2:
                    state = eye.BLINK
                    sbg = blink
                    LOGGER.info('Nextblink RESET!')
                    blinkTimer = time.time()
                    nextBlink = randint(1, BLINKMAX)
                    blinkCount = 3
                    LOGGER.info('Nextblink RESET! %d', nextBlink)
                    time.sleep(0.1)
                elif blinkCount == 3:
                    sbg = neutral
                    state = eye.NEUTRAL
                    blinkCount = 0
            
            eyeDraw.draw(sbg, sfg, sleeping)
            sfg = sbg # foreground Slide set to old background
        
        if mykeys.read() == 27:
            mykeys.close()
            DISPLAY.destroy()
            listener.close()
            break
        elif mykeys.read() == 106:
            blinkTimer = time.time()
            mode == "EYE"
            sleeping = False
     
    #DISPLAY.destroy()
except BaseException:
    logging.getLogger(__name__).exception("Program terminated")
    raise
