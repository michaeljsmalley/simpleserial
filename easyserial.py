#!/usr/bin/env python2.7

###############################################################################
#
# Interactive serial connection interface
# Requires:
#   Python 2.7+
#   pyserial (http://pyserial.sourceforge.net/) -- to install run:
#     pip install pyserial
#
###############################################################################

import serial
import subprocess
from sys import platform

def interface_selection():
    # Based on the platform, get all potential serial interfaces on the system
    if platform == "darwin":
        devicestr = subprocess.check_output("ls /dev/tty.*", shell=True)
    # Convert string output to a list and remove empty items
    devicelist = filter(None, devicestr.split('\n'))

    ### Menu ###
    print "Available Serial Devices"
    print "------------------------"
    for item in enumerate(devicelist):
        print "%d - %s" % item
    try:
        choice = int(raw_input("Choose the number of the device you with to use for serial communications: "))
    except ValueError:
        print "Not a number."

    try:
        chosen = devicelist[choice]
    except IndexError:
        print "Invalid choice."

    return chosen

# Get user selection for a serial interface and initialize it
ser = serial.Serial(interface_selection(), 9600, timeout=1)
# Output the name of the desired serial interface
print "Serial connection via: " + ser.portstr
# Write to the serial interface
ser.write("writing to serial cable")
# Close the connection
ser.close() 
