import os
import glob
import time
import numpy as np

openTime = time.strftime('%b/%d/%Y-%H:%M:%S')
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

curData = []

class TEMP:
    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
 
    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c
    
    def startSession():
        d = open('incTemp1.txt', 'a+');
        d.write('\n' + 'Session Start: ' + str(openTime) + '\n\n')
        
    def curTime(): 
        return time.strftime('%b/%d/%Y-%H:%M:%S')

    def getTemp():
        if len(curData) < 1:
            startSession()
        curData.append(read_temp())
        d.write(str(read_temp())+ '\t' + curTime() + '\n')