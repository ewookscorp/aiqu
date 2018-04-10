Raspberry pi emotion eye project for ALVIN 
http://www.alvinai.com/

Run:
sudo python aiqu.py

Run on boot (optional)
1: edit /etc/rc.local
2: add followed line
   /home/pi/aiqu/runonboot.sh &

Requires:
Python, pygame, imutils


pip install imutils
pip install --upgrade imutils

OpenCV for raspberry
The first thing to do is to find out that everything is working... 
Your rpi must be connected to 
internet, and updated...
 
'''
sudo apt-get update sudo apt-get upgrade 
''' 

Install the essentials: 

''' 
sudo apt-get install python-wxgtk2.8 python-matplotlib python-opencv python-pip python-numpy
'''

Text to speech

sudo pip install pyttsx
