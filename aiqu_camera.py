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

import facedetect as face

from threading import Thread

this = sys.modules[__name__]

detect = False
global faceFound
global fx, fy

this.faceFound = False
this.t = 0
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
	this.detectStart = time.time()
	this.t = face.DetectThread(detectCB)
	this.t.start()

	while True:
		print "looppaa"
		if this.detectRunning == False:
		   dif = time.time() - this.detectStart
		   this.detectRunning = True
		   if dif >= 5:
                          print "new loop start"
                          this.detectStart = time.time()
                          this.t = face.DetectThread(detectCB)
                          this.t.start()

		#if not this.t.isAlive():
		#	print "is not alive"
		#	dif = time.time() - this.detectStart
		#	if dif >= 5:
		#	   print "new loop start"
		#	   this.detectStart = time.time()
		#	   this.t = face.DetectThread(detectCB)
		#	   this.t.start()
		#else:
		#   print "live"

#Start camera looping
main()
