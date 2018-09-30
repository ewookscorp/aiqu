#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" Peter Hess' converted shader for pi3d dynamic texturing """
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

sys.path.insert(1, '/home/pi/aiqu')
os.putenv('SDL_FBDEV', '/dev/fb1')
this = sys.modules[__name__]

#Variables are defined here
this.BLINKMAX = 10
this.nextBlink = 0
this.blinkTimer = 0
this.blinkCount = 0

this.state = eye.NEUTRAL
this.oldState = state

this.LOGGER = pi3d.Log(level='DEBUG', file='aiqu.log')

# Load textures
this.neutral = pi3d.Texture("textures/eyes/neutral.png")
this.blink = pi3d.Texture("textures/eyes/blink.png")
this.patimg = pi3d.Texture("textures/PATRN.PNG")
this.coffimg = pi3d.Texture("textures/COFFEE.PNG")

def tex_load(fname):
  ''' return a slide object
  '''
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
  

class Slide(object):
  def __init__(self):
    self.tex = None
    self.dimensions = None
	
	
	
def eyeDraw():
	#BLINK ANIMATE
	
	dif =  time.time() - this.blinkTimer
	LOGGER.info('DIF %s', dif)
	LOGGER.info('STATE %s', this.state)
	
	if dif >= this.nextBlink and this.blinkCount == 0 and this.state != eye.DOUBT:
		this.oldState = this.state
		this.state = eye.BLINK
		#this.sbg = this.blink
		this.blinkCount = this.blinkCount +1
	elif this.blinkCount == 1:
		this.state = this.oldState
		#this.sbg = this.neutral
		this.blinkCount = this.blinkCount +1
	elif this.blinkCount == 2:
		this.state = eye.BLINK
		#this.sbg = this.blink
		this.blinkStart = time.time()
		this.nextBlink = randint(1, BLINKMAX)
		this.blinkCount = 3
	elif this.blinkCount == 3:
		this.state = eye.NEUTRAL
		#this.sbg = this.neutral
		this.blinkCount = 0
	
	#BLINK ANIMATE DONE
	
####################### FUNCTIONS DEFINES END#######################################
#DISPLAY = pi3d.Display.create(x=50, y=50)
DISPLAY = pi3d.Display.create()
DISPLAY.set_background(0, 0, 0, 1) # r,g,b,alpha

# eyeRadius is the size, in pixels, at which the whole eye will be rendered.
if DISPLAY.width <= (DISPLAY.height * 2):
	# For WorldEye, eye size is -almost- full screen height
	eyeRadius   = DISPLAY.height / 2.1
else:
	eyeRadius   = DISPLAY.height * 2 / 5


#cam = pi3d.Camera(is_3d=False, at=(0,0,0), eye=(0,0,-1000))
#shader = pi3d.Shader("uv_light")
shader = pi3d.Shader("2d_flat")
light  = pi3d.Light(lightpos=(0, -500, -500), lightamb=(0.2, 0.2, 0.2))

eyePlane = pi3d.Plane(w=DISPLAY.width, h=DISPLAY.height, name="eyeplane", z=12)



xrat = DISPLAY.width/neutral.ix
yrat = DISPLAY.height/neutral.iy
if yrat < xrat:
  xrat = yrat
wi, hi = neutral.ix * xrat, neutral.iy * xrat
#wi, hi = tex.ix, tex.iy
xi = (DISPLAY.width - wi)/2
yi = (DISPLAY.height - hi)/2

#Create canvas 
canvas = pi3d.Canvas()
canvas.set_shader(shader)


this.blinkStart = time.time()

this.sbg = this.neutral #tex_load("textures/eyes/neutral.png")

mykeys = pi3d.Keyboard()
while DISPLAY.loop_running():

  eyeDraw()
  sfg = this.sbg # foreground Slide set to old background
  canvas.set_draw_details(canvas.shader,[sfg.tex, this.sbg.tex]) # reset two textures
  canvas.set_2d_size(this.sbg.dimensions[0], this.sbg.dimensions[1], this.sbg.dimensions[2], this.sbg.dimensions[3])
  canvas.unif[48:54] = canvas.unif[42:48] #need to pass shader dimensions for both textures
  canvas.set_2d_size(this.sfg.dimensions[0], this.sfg.dimensions[1], this.sfg.dimensions[2], this.sfg.dimensions[3])
  canvas.draw()
 
  
  if mykeys.read() == 27:
    mykeys.close()
    DISPLAY.destroy()
    break