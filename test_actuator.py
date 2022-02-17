import serial
import time

ard = serial.Serial(port='COM13', baudrate=115200)

def drive_demo ():
    while True:
        for i in range(100,200): ard.write([101,i,1,0]); time.sleep(0.02)
        for i in range(100,200): ard.write([101,i,0,1]); time.sleep(0.02)
        for i in range(100,200): ard.write([101,i,1,1]); time.sleep(0.02)
        for i in range(100,200): ard.write([101,i,0,0]); time.sleep(0.02)
        for i in range(100,200): ard.write([101,i,1,2]); time.sleep(0.02)
        for i in range(100,200): ard.write([101,i,0,2]); time.sleep(0.02)
        for i in range(100,200): ard.write([101,i,2,1]); time.sleep(0.02)
        for i in range(100,200): ard.write([101,i,2,0]); time.sleep(0.02)
drive_demo()
