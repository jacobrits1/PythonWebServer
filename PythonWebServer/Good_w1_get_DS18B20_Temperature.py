# -*- coding: utf-8 -*
import os
import glob
import time
import subprocess
import platform
#din = GPIO4 (Pin 7)
#このソフトを実行する前に、温度計モジュールを接続する
#そうでないと、
#modprobe: ERROR: could not insert 'w1_therm': Operation not permitted
#が出る

device_file=''

def init_temp():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file1 = device_folder + '/w1_slave'
    return device_file1

def read_temp_raw():
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
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
        return temp_c, temp_f
def temp_main():
    while True:
        s = "celsius: {0:.3f}, fahrenheit: {1:.3f}"
        temp = read_temp()
        print(s.format(*temp))
        time.sleep(2)

platform_system=platform.system()
if platform_system != 'Windows':
    device_file=init_temp()

if __name__ == "__main__":
    try:
        temp_main()
    except KeyboardInterrupt:
        pass

