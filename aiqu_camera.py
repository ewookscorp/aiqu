'''
Created on 4.3.2018

@author: Sami<sami@tabloiti.com>
Aiqu camera loop, this part is runned in bacground

'''

import pygame
import os
import select
import sys
import time
from time import sleep
import botutils
import emotiondraw as eye
from random import randint
import config
import weatherdraw as ws

import camerathread

from threading import Thread

this = sys.modules[__name__]

detect = False
global faceFound
global fx, fy

this.faceFound = False
this.t = None
this.detectRunning = False

#
#
# Callback for facedetect
#
#
def detectCB(result, x, y, motion, pos):
		print "Detect result: " + str(result)
		print "Face x:" + str(x) + " y:" + str(y)
		global faceFound
		global fx, fy
		fx = x
		fy = y
		faceFound = result
		this.detectRunning = False
		
#--------------------------------------------------------------------------------------------------
#
# MAIN PROGRAM
#
#--------------------------------------------------------------------------------------------------
def main():

	#this.detectStart = time.time()
	#this.t = detect.DetectThread(detectCB)
	#this.t.start()
	camerathread.startCamera(detectCB)
	
	#Main code
	pygame.init()
	infoObject = pygame.display.Info()

	H = infoObject.current_h
	W = infoObject.current_w
	#print infoObject
	if config.ROTATE:
        #320, 480
		lcd = pygame.display.set_mode((H, W), pygame.FULLSCREEN)
	else:
		lcd = pygame.display.set_mode((W, H), pygame.FULLSCREEN)

	while True:
		i,o,e = select.select([sys.stdin],[],[],0.0001)
		for s in i:
			if s == sys.stdin:
				input = sys.stdin.readline()
				if input.startswith('e'):
					#this.t.setTerminated()
					print("Bye Bye!")
					raise SystemExit
		pygame.display.update()
	

#Start camera looping
main()
