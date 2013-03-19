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

def stopbits_convert(value):
    ''' Converts value to constant understood by pyserial'''
    if value=="1":
        stopbits = serial.STOPBITS_ONE
    elif value=="1.5":
        stopbits = serial.STOPBITS_ONE_POINT_FIVE
    elif value=="2":
        stopbits = serial.STOPBITS_TWO
    else:
        stopbits = stopbits_convert(generate_menu("Available Stopbits", ['1', '1.5', '2'], "Choose a stopbits value"))

    return stopbits

def parity_convert(parityvalue):
    if parityvalue in ("None", "none", "NONE", "N", "n"):
        parity = serial.PARITY_NONE
    elif parityvalue in ("Even", "even", "EVEN", "E", "e"):
        parity = serial.PARITY_EVEN
    elif parityvalue in ("Odd", "odd", "ODD", "O", "o"):
        parity = serial.PARITY_ODD
    else:
        parity = parity_convert(generate_menu("Available Parities", ['None', 'Even', 'Odd'], "Choose a parity"))

    return parity

def generate_menu(title, options, promptmsg):
    print title
    print "=" * len(title)
    for option in enumerate(options):
        print "%d - %s" % option
    try:
        choice = int(raw_input(promptmsg + ": "))
    except ValueError:
        print "Not a valid choice."

    try:
        chosen = options[choice]
    except IndexError:
        print "Invalid choice."

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

def simpleserial():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='A simple serial connection handler.')
    parser.add_argument('-i', '--interface', dest='interface', type=str, help='path to a serial interface, (e.g. /dev/tty.interfacename)')
    parser.add_argument('-r', '--baudrate', dest='baudrate', help='Desired baud rate, (e.g. 9600)')
    parser.add_argument('-d', '--databits', dest='databits', type=str, help='Desired data bits (e.g. 5, 6, 7 or 8)')
    parser.add_argument('-s', '--stopbits', dest='stopbits', type=str, help='Desired stop bits (e.g. 1, 1.5, or 2)')
    parser.add_argument('-p', '--parity', dest='parity', type=str, help='Desired parity (e.g. None, Even, Odd, Mark, or Space)')
    parser.add_argument('-f', '--flowcontrol', dest='flowcontrol', type=str, help='Flow control on or off')
    parser.add_argument('-a', '--handshake', dest='handshake', type=str, help='Hardware handshake on or off')
    parser.add_argument('-m', '--message', dest='message', type=str, help='Message to send over the serial connection')
    args = parser.parse_args()

    # Get value or user selection for serial connection properties and initialize it
    interface = args.interface if args.interface else generate_menu("Available Serial Devices", get_interfaces(), "Choose an interface")
    baudrate = args.baudrate if args.baudrate else generate_menu("Available Baud Rates", [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 56000, 57600, 115200], "Choose a baud rate")
    databits = args.databits if args.databits else generate_menu("Available Databits", [7, 8], "Choose a databits setting: ")
    stopbits = stopbits_convert(args.stopbits)
    parity = parity_convert(args.parity)

    if args.flowcontrol in ("0", "none", "NONE", "N", "n", "No", "Off", "off"):
        flowcontrol = "Off"
    elif args.flowcontrol in ("1", "Yes", "yes", "On", "on"):
        flowcontrol = "On"
    else:
        flowcontrol = generate_menu("Available Flow Controls", ["Off", "On"], "Flow control on or off")
    # handshake = args.handshake if args.handshake else generate_menu("Hardware handshake Off or On?", ["Off", "On"], "Hardware handshake be on or off")

    if args.message:
        message = args.message
    else:
        print "Please enter a message to send over the serial connection (press [Enter] when finished):"
        message = raw_input("> ")


    # Assign values to ser object
    ser = serial.Serial()
    ser.port = interface
    ser.baudrate = baudrate
    ser.bytesize = int(databits)
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
    ser.write(message+'\r')
    ser.flush()
    # Read return value
    print ser.read(1)
    # Close the connection
    ser.close()

if __name__ == '__main__':
    simpleserial()
