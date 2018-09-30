import os
import sys
import time
from multiprocessing import Process, Queue

print "Erkki"

def reader(queue):
	## Read from the queue
	while True:
		msg = queue.get()  
		print msg# Read from the queue and do nothing
		if (msg == 'DONE'):
			break


queue = Queue()
reader_p = Process(target=reader, args=((queue),))
reader_p.daemon = True
reader_p.start()
