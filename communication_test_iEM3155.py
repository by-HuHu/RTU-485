#!/usr/bin/env python

import os                   #Provides a portable way of using operating system dependent functionality
import numpy as np
import serial
import time
import datetime
import minimalmodbus

minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
minimalmodbus.HANDLE_LOCAL_ECHO = False

instr = minimalmodbus.Instrument('COM16', 1, mode = 'rtu')  
#Port name, Slave adress (decimal), mode (RTU or ASCII)
#port(str): The serial port name, for example /dev/ttyUSB0 (Linux), /dev/tty.usbserial (OS X) or COM4 (Windows).

instr.serial.baudrate = 19200
instr.serial.bytesize = 8
instr.serial.stopbits = 1
instr.serial.parity = serial.PARITY_EVEN
instr.serial.timeout  = 0.2
instr.debug = False	

while True:
    try:
        print(instr.read_register(3016,0,4,signed=False))				
        #(registeraddress, numberOfDecimals=0, functioncode=3, signed=False)
        print(instr.read_register(20,0,4))
        i=i+1
        print(i)
    except IOError:
        print("Failed to read from instrument")
    


