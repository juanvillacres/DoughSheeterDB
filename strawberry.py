# Give the path to find the python wrapper
import sys
sys.path.append('phidgetsClass/')
sys.path.append('laserClass/')

# Import modules
from threading import Thread
from datetime import datetime
import time
import os
import signal
import sys

# Import the wrapped API
import phidgetsClass_ext
import laserClass_ext

#######################################
# To manage interruption
#######################################
def signal_handler(signal, frame):
        print('Stop the system!')
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	laser0.stopAcquisition()
	laser1.stopAcquisition()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#######################################
# Create the lasers and phidgets objects
#######################################

# Create the laser object
laser0=laserClass_ext.laserClass(0)
laser1=laserClass_ext.laserClass(1)

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()
results = phidgets.initConnection()
if results > 0:
	phidgets.cleanConnection()
	sys.exit(0)

####################
# INIT
####################

# Init the stepper motor
#phidgets.initStepper()

# Create a new main directory
expDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)
 
####################
# RUN THE EXPERIMENT
####################

####################
# 1 - Move the stepper motor (Wait for the motor to reach its final position)
print "Move the stepper"
#phidgets.moveStepper(10)

####################
# 2 - Start laser #0
print "Start laser 0"
# Setup the filename to save the current data
laser0.set_fileName(expPath + "data0.xyz")
# Setup the parameters to save the data
laser0.set_save()
# Create a thread for the laser
thread_l = Thread(target=laser0.grabAndSave, args=(0,))
# Start the thread
thread_l.start()

####################
# 2.1 - Start load cells
#phidgets.set_lcFileName(expPath + "lc0.txt")

#thread_lc = Thread(target=phidgets.loadCells, args=())
#thread_lc.start()

#######################
# 3 - Start the rollers
print "Start the rollers"
#thread_r = Thread(target=phidgets.runMotorsLoop, args=(-1,60,))
#thread_r.start()

#########################
# 4 - Start the conveyors
print "Start the conveyors"
phidgets.runConveyors(0,40,1,0)

#########################
# WAIT !!!!!!!!!!!
# Data acquisition
while laser0.get_acquisition() == True:
	dumb = 1
print "End of acquisition 1"

#########################
# 5 - Stop laser #0
#print "Stop laser"
#laser0.stopAcquisition()

#########################
# 5.1 - Stop load cells
#phidgets.stopLoadCells()

#########################
# 6 - Stop the rollers
#print "Stop motors"
#phidgets.stopMotorsLoop()

#########################
# 7 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()

#########################
# Change direction !!!!!!!!!!!!!
time.sleep(1)
print "Change direction"
#########################


