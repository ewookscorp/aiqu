import io
import picamera
import cv2
import os
import numpy
import time
import threading
from threading import Thread
import config
import imutils
import sys
import tempfile

from imutils.video import VideoStream
from imutils.video import FPS

from picamera.array import PiRGBArray
from picamera import PiCamera


this = sys.modules[__name__]
	
this.motionDetect = False

#motion place: LEFT, RIGHT, CENTER, UP, DOWN
this.motionPlace = "CENTER"

class DetectThread(Thread):
	detected = False
	sleeping = False
	
	def getState():
		self.detected
	
	def setState(self, state):
		self.sleeping = state

	def __init__( self, callback):
		Thread.__init__(self)
		self.callback = callback
		#self.detectWork()

	def run( self ):
		detectWork(self.callback, self, self.sleeping)
        #self.callback(self.detected)
		# ... Clean shutdown code here ...
		print('Thread #%s stopped' % self.ident)

#all other funtions 
			
def motion(gray, color):
	print "SLEEP TRY FIND MOTION"
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	last = cv2.imread(config.TEMP_PATH +"/motion.jpg")
	height, width = last.shape[:2]
	last = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
	last = cv2.GaussianBlur(last, (21, 21), 0)

	#cv2.imwrite(config.TEMP_PATH+ "/blur.jpg", gray)

	#calculate difrence between two frames
	frameDelta = cv2.absdiff(gray, last)
	thresh = cv2.threshold(frameDelta, config.delta_thresh, 255, cv2.THRESH_BINARY)[1]   

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	xp = 0
	yp = 0
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < config.min_area:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		#cv2.rectangle(color, (x, y), (x + w, y + h), (255, 255, 0), 2)
		cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 0), 2)

		cv2.imwrite(config.TEMP_PATH+ "/blur.jpg", gray)
		cv2.imwrite(config.TEMP_PATH+ "/motion2.jpg",color)

		print "BOX X: " ,x
		print "BOX Y: ", y
		xp = x
		yp = y
#240/3
     
	s = frameDelta.sum()
	print s
	
	if s > config.motionsense:
		this.motionDetect = True
	else:
		this.motionDetect = False
		
	#cv2.imwrite(config.TEMP_PATH+ "/blur.jpg", gray)
	#cv2.imwrite(config.TEMP_PATH+ "/motion2.jpg",color)
	cv2.imwrite(config.TEMP_PATH+ "/motion.jpg",color)

def startStrem():
	this.stream = io.BytesIO()

	#Get the picture (low resolution, so it should be quite fast)
	#Here you can also specify other parameters (e.g.:rotate the image)
	with picamera.PiCamera() as camera:
		camera.resolution = (320, 240)
		camera.brightness = config.BRIGHTNES
		camera.awb_mode = config.AWB
		camera.exposure_mode = 'auto'
		#camera.awb_gains = (1.0, 1.0)
		camera.capture(this.stream, format='jpeg', use_video_port=True)
		camera.start_preview()
	
		
def detect(cb, sleeping):
	print "start detect, state", sleeping
	faces = 0
	faceX = 0
	faceY = 0
	faceW = 0
	faceH = 0
	this.motionDetect = False
	
	#this.stream = io.BytesIO()
	#with picamera.PiCamera() as camera:
	#	camera.resolution = (320, 240)
	#	camera.framerate = 32
	#	rawCapture = PiRGBArray(camera, size=(320, 240))
	#	stream = camera.capture_continuous(this.stream, format="bgr", use_video_port=True)
	

	#Create a memory stream so photos doesn't need to be saved in a file

	#camera.rotation = 90

	#Convert the picture into a numpy array
	buff = numpy.fromstring(this.stream.getvalue(), dtype=numpy.uint8)

	#Now creates an OpenCV image
	image = cv2.imdecode(buff, 1)
	#image = cv2.imdecode(frame, 1)
	image = imutils.rotate(image, config.IMGROTATE)

	#Load a cascade file for detecting faces
	#face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
	#face_cascade = cv2.CascadeClassifier('/home/pi/botty/face/haarcascade_frontalface_alt.xml')
	face_cascade = cv2.CascadeClassifier('/home/pi/botty/xml/face.xml')
	#profileface_cascade = cv2.CascadeClassifier('/home/pi/botty/haarcascade_profileface.xml')
	

	#Convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#if we are sleeping try wakeup by motion detect
	if sleeping == True:
		motion(gray, image)
	else:
		print "Try face detect"
		#Look for faces in the image using the loaded cascade file
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)

		print "Found "+str(len(faces))+" face(s)"

		#Draw a rectangle around every found face
		
		for (x,y,w,h) in faces:
			cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
			faceX = x
			faceY = y
			faceW = w
			faceH = h
		print "Save img face"
		cv2.imwrite(config.TEMP_PATH+ "/face.jpg",image)
		
		Cface = [(faceW/2+faceX),(faceH/2+faceY)] #check the motion position on image
		print Cface

		if Cface[0] != 0:
			if Cface[0] > 180:
				print "LEFT"
				this.motionPlace = "LEFT"
				
			if Cface[0] < 140:
				print "RIGHT"
				this.motionPlace = "RIGHT"
				
			if Cface[1] > 140:
				print "DOWN"
				this.motionPlace = "DOWN"
			if Cface[1] < 100:
				print "UP"
				this.motionPlace = "UP"

	#Save the result image
	
	#if config.DEBUG or sleeping == True:
	#cv2.imwrite(config.TEMP_PATH+ "/face.jpg",image)
	
	#if sleeping == True:
	print "Save img motion"
	cv2.imwrite(config.TEMP_PATH+ "/motion.jpg",gray)

	if sleeping == True:
		detected = False
		cb(False, faceX, faceY, this.motionDetect, this.motionPlace)
	elif len(faces) >= 1:
		detected = True
		cb(True, faceX, faceY, this.motionDetect, this.motionPlace)
	else:
		detected = False
		cb(False, faceX, faceY, this.motionDetect, this.motionPlace)
			
def detectWork(cb, self, sleeping):
	#while True:
	detect(cb, sleeping)

	#self.callback(self.detected)	
	#time.sleep(2)

startStrem()
