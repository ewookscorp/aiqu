import io
import picamera
import cv2
import numpy
import time
import threading
from threading import Thread

	
class DetectThread(Thread):
	detected = False
	
	def getState():
		self.detected

	def __init__(self, callback):
        	Thread.__init__(self)
        	self.callback = callback
		#self.detectWork()

    	def run(self):
			detectWork(self.callback, self)
        	#self.callback(self.detected)
			# ... Clean shutdown code here ...
			print('Thread #%s stopped' % self.ident)
			
def detect(cb):
	print "start detect"
	#Create a memory stream so photos doesn't need to be saved in a file
	stream = io.BytesIO()

	#Get the picture (low resolution, so it should be quite fast)
	#Here you can also specify other parameters (e.g.:rotate the image)
	with picamera.PiCamera() as camera:
		camera.resolution = (320, 240)
		camera.capture(stream, format='jpeg')

	#Convert the picture into a numpy array
	buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

	#Now creates an OpenCV image
	image = cv2.imdecode(buff, 1)

	#Load a cascade file for detecting faces
	#face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
	#face_cascade = cv2.CascadeClassifier('/home/pi/botty/face/haarcascade_frontalface_alt.xml')
	face_cascade = cv2.CascadeClassifier('/home/pi/botty/xml/face.xml')


	#Convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#Look for faces in the image using the loaded cascade file
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)

	print "Found "+str(len(faces))+" face(s)"

	#Draw a rectangle around every found face
	faceX = 0
	faceY = 0
	for (x,y,w,h) in faces:
		cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
		faceX = x
		faceY = y

	#Save the result image
	cv2.imwrite('result.jpg',image)

	if len(faces) >= 1:
		detected = True
		cb(True, faceX, faceY)
	else:
		detected = False
		cb(False, faceX, faceY)
			
def detectWork(cb, self):
	#while True:
	detect(cb)

	#self.callback(self.detected)	
	#time.sleep(2)
