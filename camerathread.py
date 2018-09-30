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
import numpy as np
import sys
import mmap
import json

#import sysv_ipc
#from multiprocessing.connection import Client


this = sys.modules[__name__]    
this.motionDetect = False

#motion place: LEFT, RIGHT, CENTER, UP, DOWN
this.motionPlace = "CENTER"
this.cbres = None

done = False
lock = threading.Lock()
pool = []

class DetectThread(threading.Thread):
    def __init__(self):
        super(DetectThread, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        global frames
        global start
        global done
        global grayback
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    #if is_changed(config):
                    #    config = reload(config)
                    minpixel=1
                    self.stream.seek(0)
                    frames+=1
                    currentframe=frames ## Because frame can be incremented by other threads while proccesing
                    sleeping = False
                    # Read the image and do some processing on it
                    # Construct a numpy array from the stream
                    data = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
                    # "Decode" the image from the array, preserving colour
                    image = cv2.imdecode(data, 1)

                    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                    
                     #read from IPC
                    #FOR IPC Process
                    pipe_name = '/tmp/aiqumotionpipe'
                    pipein = open(pipe_name, 'r')
                    line = pipein.readline()[:-1]
                   
                    time.sleep(0.2)
                    if not line:
                        print('FILE IS EMPTY')
                    else: 
                        #print "Read Line: %s" % (line)
                        if "1" in line:
                            #print "SLEEP"
                            sleeping = True
                        else:
                            sleeping = False
                    time.sleep(0.2)  
                    pipein.close()
                    self.detect(None, sleeping, image, gray)
            
                    finish = time.time()
                    #print('Captured %d frames at %.2ffps' % (
                    #        currentframe,
                    #        currentframe / (finish - start)))
                    #...
                    #...
                    # Set done to True if you want the script to terminate
                    # at some point
                    #done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)
    
    ####### OLD BELLOW ############
            
    def motion(self, gray, color):
        motionDetect = False
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
        print "Write motion.jpg"        
        cv2.imwrite(config.TEMP_PATH+ "/motion.jpg",color)
        time.sleep(0.2)
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        xp = 0
        yp = 0
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            #print ("AREA:", cv2.contourArea(c))
            if cv2.contourArea(c) < config.min_area:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(color, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 0), 2)

            cv2.imwrite(config.TEMP_PATH+ "/blur.jpg", gray)
            cv2.imwrite(config.TEMP_PATH+ "/motion2.jpg",color)

            print "BOX X: " ,x
            print "BOX Y: ", y
            xp = x
            yp = y

        s = frameDelta.sum()
        print "MOTION SENSE:" ,s
        
        if s > config.motionsense:
            self.motionDetect = True
        else:
            self.motionDetect = False
            
        #cv2.imwrite(config.TEMP_PATH+ "/blur.jpg", gray)
        #cv2.imwrite(config.TEMP_PATH+ "/motion2.jpg",color)
        print "MOTION ", self.motionDetect
        return self.motionDetect
    
    def sendMessage(self,msg):
        #print "SENDIN MESSAGE!"
    
        try:
            #FOR IPC Process
            pipe_name = '/tmp/aigupipe'
            pipeout= open(pipe_name, 'w')
            pipeout.write(msg)
            pipeout.close()
        except ValueError:
            print "ERR! ", ValueError 
        
    
    '''
    def startStrem(self):
        this.stream = io.BytesIO()

        #Get the picture (low resolution, so it should be quite fast)
        #Here you can also specify other parameters (e.g.:rotate the image)
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)
            camera.brightness = config.BRIGHTNES
            camera.awb_mode = config.AWB
            camera.exposure_mode = 'auto'
            camera.capture(this.stream, format='jpeg', use_video_port=false)
            camera.start_preview()
    '''        
            
    def detect(self, cb, sleeping, image, gray):
        #print "start detect, state", sleeping
        faces = 0
        faceX = 0
        faceY = 0
        faceW = 0
        faceH = 0
        self.motionDetect = False
        detected = False
        

        #Load a cascade file for detecting faces
        face_cascade1 = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
        face_cascade2 = cv2.CascadeClassifier('/home/pi/botty/face/haarcascade_frontalface_alt.xml')
        face_cascade3 = cv2.CascadeClassifier('/home/pi/botty/xml/face.xml')
        profileface_cascade = cv2.CascadeClassifier('/home/pi/botty/haarcascade_profileface.xml')
        
        #if we are sleeping try wakeup by motion detect
        if sleeping == True:
            this.motionDetect = self.motion(gray, image)
            cv2.imwrite(config.TEMP_PATH+ "/face.jpg",image)
        else:
            print "Try face detect"
            this.motionDetect = False
            #Look for faces in the image using the loaded cascade file
            faces = face_cascade3.detectMultiScale(gray, 1.1, 5)
            
            if(len(faces)<=0):
                faces = face_cascade1.detectMultiScale(gray, 1.1, 5)
            if(len(faces)<=0):
                faces = face_cascade2.detectMultiScale(gray, 1.1, 5)
            if(len(faces)<=0):    
                faces = profileface_cascade.detectMultiScale(gray, 1.1, 5)
                
            print "Found "+str(len(faces))+" face(s)"
            #if len(faces) > 0:
            #    print "FACE FOUND!"
            #Draw a rectangle around every found face
            
            for (x,y,w,h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
                faceX = x
                faceY = y
                faceW = w
                faceH = h
                
            #print "Save img face"
            cv2.imwrite(config.TEMP_PATH+ "/face.jpg",image)
            time.sleep(0.2)
            Cface = [(faceW/2+faceX),(faceH/2+faceY)] #check the motion position on image
            #print Cface

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

        #print "Save img motion"
        #
        cv2.imwrite(config.TEMP_PATH+ "/motion.jpg",gray)
        time.sleep(0.2)
        #if cb == None:
            #print "Callback not defined"
            #done = True
            
        if sleeping == True:
            detected = False
            #cb(False, faceX, faceY, self.motionDetect, self.motionPlace)
            #self.sendMessage(detected)
        elif len(faces) >= 1:
            detected = True
            #if cb != None:
                #cb(True, faceX, faceY, self.motionDetect, self.motionPlace)
            #self.sendMessage(detected)
        else:
            detected = False
            #self.sendMessage(detected)
            #if cb != None:
                #cb(False, faceX, faceY, self.motionDetect, self.motionPlace)
            
        #msg = "{motion:" + (str)this.motionDetect + ",facedetect:" + (str)detected +",motionplace:+"+ this.motionPlace+ "}"
        
        if detected:
            print "MOTION DETECTED!!"
        
        data = {}
        data['motion'] = this.motionDetect
        data['face'] = detected
        data['posit'] = this.motionPlace
        self.sendMessage(json.dumps(data))
        
    def detectWork(cb, self, sleeping):
        detect(cb, sleeping)

                    
#all other funtions 
def streams():
    while not done:
        with lock:
            if pool:
                #print "Prosessor POOOL"
                processor = pool.pop()
            else:
                #print "Prosessor NONE"
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            #print ("Waiting")            
            time.sleep(0.1)

            
with picamera.PiCamera() as camera:
    pool = [DetectThread() for i in range(1)]

    print ("Starting fixed settings setup")
    #camera.resolution = (1280, 720)
    camera.resolution = (320, 240)
    #camera.framerate = 30
    #camera.brightness = config.BRIGHTNES
    #camera.awb_mode = config.AWB
    #camera.exposure_mode = 'auto'
    # Wait for analog gain to settle on a higher value than 1
    #while camera.analog_gain <= 1:
    #    time.sleep(0.1)
    '''
    print ("Fixing the values")
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    '''
    #camera.start_preview()
    time.sleep(2)
    backstream = io.BytesIO()
    camera.capture(backstream,format='jpeg', use_video_port=True)
    databack = np.fromstring(backstream.getvalue(), dtype=np.uint8)
    # "Decode" the image from the array, preserving colour
    background = cv2.imdecode(databack, 1)
    grayback = cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('background'+".png",background)

    start = time.time()
    frames=0
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    try:
        with lock:
            processor = pool.pop()
        processor.terminated = True
        processor.join()
    except KeyboardInterrupt:
        print "Ctrl-c pressed ..."
        sys.exit(1)