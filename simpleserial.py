#!/usr/bin/env python2.7

###############################################################################
#
# simpleserial.py - Michael J. Smalley
#
# Interactive serial connection interface
#
# Requires:
#   Python 2.7+
#   pyserial (http://pyserial.sourceforge.net/) -- to install run:
#     pip install pyserial
#
###############################################################################

import argparse
import serial
import subprocess
from sys import platform

def get_interfaces():
    # Based on the platform, get all potential serial interfaces on the system
    if platform == "darwin":
        devicestr = subprocess.check_output("ls /dev/tty.*", shell=True)
    # Convert string output to a list and remove empty items
    devicelist = filter(None, devicestr.split('\n'))

    return devicelist

def interface_selection():

    devicelist = get_interfaces()

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

    print chosen
    return chosen

def baudrate_selection():
    print "Available Baud Rates"
    print "===================="
    baudrates = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 56000, 57600, 115200]
    for item in enumerate(baudrates):
        print "%d - %s" % item
    try:
        choice = int(raw_input("Choose the baud rate you would like to use for serial communications: "))
    except ValueError:
        print "Not a number."

    try:
        chosen = baudrates[choice]
    except IndexError:
        print "Invalid baud rate."

    return chosen

def databits_selection():
    print "Available Data Rates"
    print "===================="
    databits = [7, 8]
    for item in enumerate(databits):
        print "%d - %s" % item
    try:
        choice = int(raw_input("Choose the data bits you would like to use for serial communications: "))
    except ValueError:
        print "Not a number."

    try:
        chosen = databits[choice]
    except IndexError:
        print "Invalid data bits."

    return chosen

def stopbits_selection():
    print "Available Stopbits"
    print "=================="
    stopbits = ['1','1.5', '2']
    for item in enumerate(stopbits):
        print "%d - %s" % item
    try:
        choice = int(raw_input("Choose the stopbits you would like to use for serial communications: "))
    except ValueError:
        print "Not a number."

    try:
        chosen = stopbits[choice]
    except IndexError:
        print "Invalid stopbits choice."

    return chosen

def parity_selection():
    print "Available Parities"
    print "=================="
    parities = ['None','Even', 'Odd']
    for item in enumerate(parities):
        print "%d - %s" % item
    try:
        choice = int(raw_input("Choose the parity you would like to use for serial communications: "))
    except ValueError:
        print "Not a number."

    try:
        chosen = parities[choice]
    except IndexError:
        print "Invalid parity."

    return chosen

def flowcontrol_selection():
    print "Flow Control On or Off?"
    print "======================="
    flowcontrol = ['Off', 'On']
    for item in enumerate(flowcontrol):
        print "%d - %s" % item
    try:
        choice = int(raw_input("Choose whether Flow Control should be on or off for serial communications: "))
    except ValueError:
        print "Not a number."

    try:
        chosen = flowcontrol[choice]
    except IndexError:
        print "Invalid flow control choice."

    return chosen

def handshake_selection():
    print "Hardware handshake On or Off?"
    print "======================="
    handshake = ['Off', 'On']
    for item in enumerate(handshake):
        print "%d - %s" % item
    try:
        choice = int(raw_input("Choose whether Hardware Handshake should be on or off for serial communications: "))
    except ValueError:
        print "Not a number."

    try:
        chosen = handshake[choice]
    except IndexError:
        print "Invalid hardware handshake choice."

    return chosen

def message_prompt():
    print "Please enter a message to send over the serial connection (press [Enter] when finished):"
    message = raw_input("> ")

    return message

# Set up command line argument parser
parser = argparse.ArgumentParser(description='A simple serial connection handler.')
parser.add_argument('-i', '--interface', dest='interface', type=str, help='path to a serial interface, (e.g. /dev/tty.interfacename)')
parser.add_argument('-r', '--baudrate', dest='baudrate', help='Desired baud rate, (e.g. 9600)')
parser.add_argument('-d', '--databits', dest='databits', type=int, help='Desired data bits (e.g. 5, 6, 7 or 8)')
parser.add_argument('-s', '--stopbits', dest='stopbits', type=str, help='Desired stop bits (e.g. 1, 1.5, or 2)')
parser.add_argument('-p', '--parity', dest='parity', type=str, help='Desired parity (e.g. None, Even, Odd, Mark, or Space)')
parser.add_argument('-f', '--flowcontrol', dest='flowcontrol', type=str, help='Flow control on or off')
parser.add_argument('-a', '--handshake', dest='handshake', type=str, help='Hardware handshake on or off')
parser.add_argument('-m', '--message', dest='message', type=str, help='Message to send over the serial connection')
args = parser.parse_args()

# Get value or user selection for serial connection properties and initialize it
interface = args.interface if args.interface else interface_selection()

baudrate = args.baudrate if args.baudrate else baudrate_selection()

databits = args.databits if args.databits else databits_selection()

if args.stopbits=="1":
    stopbits = serial.STOPBITS_ONE
elif args.stopbits=="1.5":
    stopbits = serial.STOPBITS_ONE_POINT_FIVE
elif args.stopbits=="2":
    stopbits = serial.STOPBITS_TWO
else:
    stopbits = stopbits_selection()

if args.parity in ("None", "none", "NONE", "N", "n"):
    parity = serial.PARITY_NONE
elif args.parity in ("Even", "even", "EVEN", "E", "e"):
    parity = serial.PARITY_EVEN
elif args.parity in ("Odd", "odd", "ODD", "O", "o"):
    parity = serial.PARITY_ODD
else:
    parity = parity_selection()

if args.flowcontrol in ("0", "none", "NONE", "N", "n", "No", "Off", "off"):
    flowcontrol = 0
elif args.flowcontrol in ("1", "Yes", "yes", "On", "on"):
    flowcontrol = 1
else:
    print("THIS IS BORKEN!")
    flowcontrol = flowcontrol_selection()

if args.message:
    message = args.message
else:
    message = message_prompt()

# handshake = args.handshake if args.handshake==None else handshake_selection()

# Assign values to ser object
ser = serial.Serial()
ser.port = interface
ser.baudrate = baudrate
ser.bytesize = databits
ser.stopbits = stopbits
ser.parity = parity
ser.xonxoff = flowcontrol
###
# STILL NEED TO IMPLEMENT HARDWARE HANDSHAKE
# if rts:
# ser.rtscts = handshake
# else if dsr:
# ser.dsrdtr = handshake
###

# Output information about the ser object
print "Serial Device: " + str(ser.name)
print "Baud Rate:     " + str(ser.baudrate)
print "Data Bits:     " + str(ser.bytesize)
print "Stop Bits:     " + str(ser.stopbits)
print "Parity:        " + str(ser.parity)
print "Flow Control:  " + str(ser.xonxoff)
print "Message:       " + str(message)
###
# STILL NEED TO IMPLEMENT HARDWARE HANDSHAKE
###
ser.open()
# Write to the serial interface
ser.write(message)
# Close the connection
ser.close() 
