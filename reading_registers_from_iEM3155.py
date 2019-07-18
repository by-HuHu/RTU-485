#!/usr/bin/env

# The script reads registers from the iEM3155 by using the Modbus RTU protocol
# Register Address has to be the Register Address number minus 1

import serial
import time
import datetime
import minimalmodbus

minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
minimalmodbus.HANDLE_LOCAL_ECHO = False

instr = minimalmodbus.Instrument('COM16', 1 , mode = 'rtu')
# Arguments: Port name (str), Slave adress (decimal), mode (RTU or ASCII)
# Port name: The serial port name, for example /dev/ttyUSB0 (Linux), /dev/tty.usbserial (OS X) or COM4 (Windows).
instr.serial.baudrate = 19200
instr.serial.bytesize = 8
instr.serial.stopbits = 1
instr.serial.parity = serial.PARITY_NONE
instr.serial.timeout  = 1
instr.debug = False

def convert_64bit(register):
    """ Converts the varaiables from Int16 to Int64 """
    real_value = (register[0]*(2^48) + register[1]*(2^32) + register[2]*(2^16) + register[3]) / 1000.
    return (real_value)

def collect_data():
    """ Collects the varaiable from the instrument, it reads four Int16 and then it converts them into one Int64 """
    try:
        register_3204 = instr.read_registers(3203,4,3) #Total Active Energy Import -kWh-
        register_3208 = instr.read_registers(3207,4,3) #Total Active Energy Export -kWh-
        register_3220 = instr.read_registers(3219,4,3) #Total reactive Energy Import -kVARh-
        register_3224 = instr.read_registers(3223,4,3) #Total reactive Energy Export -kVARh-
        totalEaImport = convert_64bit(register_3204)
        totalEaExport = convert_64bit(register_3208)
        totalErImport = convert_64bit(register_3220)
        totalErExport = convert_64bit(register_3224)
        data = [totalEaImport, totalEaExport, totalErImport, totalErExport]
    except IOError:
            print("Failed to read from instrument")
    return (data)

while True:
    dt = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    data = collect_data()
    data_ls = [dt, str(data[0]), str(data[1]), str(data[2]), str(data[3])]
    print(data)
    data_str = ",".join(data_ls)
    print(data_str)
    time.sleep(10)

