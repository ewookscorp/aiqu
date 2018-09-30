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
from multiprocessing.connection import Listener
import select
import sys
from multiprocessing import Process, Queue

'''if config.CAMEENABLED:
	import camerathread
	#import facedetect as face
'''

sys.path.insert(1, '/home/pi/aiqu')
os.putenv('SDL_FBDEV', '/dev/fb1')
this = sys.modules[__name__]

#Variables are defined here
#Aiqu modes, EYE, RADIO, WEATHER, SLEEP, DEEP
this.mode = "EYE"

this.BLINKMAX = 10
this.nextBlink = 0
this.blinkTimer = 0
this.blinkCount = 0

this.sleepTimer = 0
this.sleeping = False

this.state = eye.NEUTRAL
this.oldState = state

this.detectTimer = 0

this.LOGGER = pi3d.Log(level='DEBUG', file='aiqu.log')



def wakeup():
	this.LOGGER.info('WAKE UP!')
	this.state = eye.NEUTRAL
	this.mode = "EYE"
	this.sleeping = False
	this.sleepTimer = time.time()


def tex_load(fname):
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
  

class Slide(object):
  def __init__(self):
    self.tex = None
    self.dimensions = None
	
	
	


# Callback for facedetect
#
def detectCB(result, x, y, motion, pos):
	this.LOGGER.info('DETECT %s', motion)
	this.LOGGER.info('FACEFOUND %s', result)
	if config.CAMEENABLED:
		global faceFound
		global fx, fy
		fx = x
		fy = y
		faceFound = result

		if motion and this.sleeping == True:
			wakeup()
			
		if this.sleeping == False:
			if pos == "LEFT":
				this.state = eye.LOOKLEFT
			elif pos == "RIGHT":
				this.state = eye.LOOKRIGHT
			elif pos == "DOWN":
				this.state = eye.LOOKDOWN
			elif pos == "UP":
				this.state = eye.LOOKUP
			else:
				this.state = eye.NEUTRAL

##############END detect callback ##################################

				
def eyeDraw():
	
	#check if switch to sleeping mode, due no action ongoing
	sleep = time.time() - this.sleepTimer
	#LOGGER.info('SLEEP %s', sleep)
	
	this.sleeping = False
	if sleep >= config.SLEEP:
		this.sleeping = True

	if this.sleeping == True:
		time.sleep(2)
		this.oldState = this.state
		this.mode = "SLEEP"
		blink_eye = this.blink 
		neutral_eye = this.neutral
		this.sbg = this.blink
	else:
		#BLINK ANIMATE
		
		dif =  time.time() - this.blinkTimer
		#LOGGER.info('DIF %s', dif)
		#LOGGER.info('STATE %s', this.state)
		#LOGGER.info('nextblink %s', this.nextBlink)
		
		blink_eye = this.blink
		neutral_eye = this.neutral
		
		if dif >= this.nextBlink and this.blinkCount == 0 and this.state != eye.DOUBT:
			this.oldState = this.state
			this.state = eye.BLINK
			#this.sbg = this.blink
			this.sbg = blink_eye #tex_load("textures/eyes/blink.png")
			this.blinkCount = this.blinkCount +1
		elif this.blinkCount == 1:
			time.sleep(0.2) 
			this.state = this.oldState
			#this.sbg = this.neutral
			this.sbg = neutral_eye #tex_load("textures/eyes/neutral.png")
			this.blinkCount = this.blinkCount +1
		elif this.blinkCount == 2:
			time.sleep(0.2)
			this.state = eye.BLINK
			#this.sbg = this.blink
			this.sbg = blink_eye #tex_load("textures/eyes/blink.png")
			this.blinkTimer = time.time()
			this.nextBlink = randint(1, BLINKMAX)
			this.blinkCount = 3
		elif this.blinkCount == 3:
			time.sleep(0.2)
			this.state = eye.NEUTRAL
			#this.sbg = this.neutral
			this.sbg = neutral_eye #tex_load("textures/eyes/neutral.png")
			this.blinkCount = 0
		
		#BLINK ANIMATE DONE
	
	'''if config.CAMEENABLED:
		if not this.dt.isAlive():
			dif =  time.time() - this.detectTimer 
			if dif >= config.DETECT_DIF:
				this.detectTimer = time.time()
				if config.CAMEENABLED:
					LOGGER.info('START NEW DETECT THREAD!!!')
					this.dt = face.DetectThread(detectCB)
					this.dt.setState(this.sleeping)
					this.dt.start()
					'''
					
def readKeys():
	i,o,e = select.select([sys.stdin],[],[],0.0001)
	for s in i:
		if s == sys.stdin:
			input = sys.stdin.readline()
			if sleeping == True:
				wakeup()
			if input.startswith('r'):
				this.state = eye.LOOKRIGHT
			if input.startswith('l'):
				this.state =  eye.LOOKLEFT
			if input.startswith('n'):
				this.state = eye.NEUTRAL
			if input.startswith('d'):
				this.state = eye.LOOKDOWN
			if	input.startswith('u'):
				this.state == eye.LOOKUP
			if input.startswith('y'):
				this.state = eye.DOUBT
			if input.startswith('h'):
				this.state = eye.HAPPY
			if input.startswith('b'):
				this.state = eye.BLINK
				
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



#xrat = DISPLAY.width/neutral.ix
#yrat = DISPLAY.height/neutral.iy
#if yrat < xrat:
#  xrat = yrat
#wi, hi = neutral.ix * xrat, neutral.iy * xrat
#wi, hi = tex.ix, tex.iy
#xi = (DISPLAY.width - wi)/2
#yi = (DISPLAY.height - hi)/2

#Create canvas 
canvas = pi3d.Canvas()
canvas.set_shader(shader)

#initialize timers
this.blinkStart = time.time()
this.sleepTimer = time.time()

#initialize camera thread
'''if config.CAMEENABLED:
	LOGGER.info('INIT DETECT THREAD!!!')
	this.detectTimer = time.time()
	this.dt = face.DetectThread(detectCB)
	this.dt.setState(this.sleeping)
	this.dt.start()'''


def messageHandler(conn):
	#this.LOGGER.info('LISTENER %s', listener.last_accepted)
	 while True:
		try:
			this.LOGGER.info('LOOPPAA')
			data = conn.recv()
			this.LOGGER.info('MESSAGE %s', data)
		except ValueError:
			this.LOGGER.info('Error in receiver:', ValueError)
	
def handler():
	this.LOGGER.info('START RECEIVER')
	address = ('localhost', 6000)# family is deduced to be 'AF_INET'
	this.listener = Listener(address, authkey=b'12345')
	this.LOGGER.info('START ACCEPT')
	this.conn = this.listener.accept()
	this.LOGGER.info('START THREADING')
	thread.start_new_thread(messageHandler, (this.conn))

def reader(queue):
	## Read from the queue
	while True:
		msg = queue.get()  
		this.LOGGER.info('MESSAGE %s', msg)# Read from the queue and do nothing
		if (msg == 'DONE'):
			break
	
# Load textures
this.neutral = tex_load("textures/eyes/neutral.png")
this.blink = tex_load("textures/eyes/blink.png")
this.patimg = tex_load("textures/PATRN.PNG")
this.coffimg = tex_load("textures/COFFEE.PNG")  


def main():
	this.sbg = this.neutral #tex_load("textures/eyes/neutral.png")

	mykeys = pi3d.Keyboard()

	#queue = Queue()   # reader() reads from queue
	#reader_p = Process(target=reader, args=((queue),))
	#reader_p.daemon = True
	#reader_p.start()        # Launch reader() as a separate python process


	while DISPLAY.loop_running():
		if (this.mode == "EYE") or (this.mode == "SLEEP"):
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
			listener.close()
			break

if __name__ == '__main__':
    main()
