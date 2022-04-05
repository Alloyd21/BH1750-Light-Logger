#!/usr/bin/python
#---------------------------------------------------------------------
#
#                        Light-Logger.py
# Read data from a BH1750 digital light sensor and log it to csv.
#
# Author : Adam Lloyd
# Date   : 5/4/2022
#
#
#---------------------------------------------------------------------
import smbus
import time

from time import sleep, strftime, time
# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def main():
    while True:
      file = open("log.csv","a")
      lightLevel=readLight()
    
      print(format(lightLevel,'.2f') + "," + strftime('%Y-%m-%d'+"+"+'%H:%M:%S')+"\n")
      file.write(format(lightLevel,'.2f') + "," + strftime('%Y-%m-%d'+","+'%H:%M:%S')+"\n")

      sleep(1)

      file.close()

if __name__=="__main__":
   main()

