"""Thermal monitoring"""

import os

def get_cpu_temp():
    """ Return CPU temperature """
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return float(f.readline()) / 1000


def get_gpu_temp():
    """ Return GPU temperature as a character string"""
    res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))

if __name__ == "__main__":
    temp = get_cpu_temp()
    print(temp)
    temp2 = get_gpu_temp()
    print(temp2)
