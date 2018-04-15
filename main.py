import sys

print(sys.path)

import time
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

from rpimonitor.monitor.stat import sample_proc_stat
from rpimonitor.display.cpu_detail import calc_and_draw_cpu_detail_text

def monitor_cpu(device, font, count=100):
    """Monitor the cpu"""
    stats = sample_proc_stat()
    cpu, cores = stats['cpu'], stats['cores']
    i = 0
    while i < count:

        time.sleep(1)

        prev_cpu, prev_cores = cpu, cores

        stats = sample_proc_stat()
        cpu, cores = stats['cpu'], stats['cores']
        calc_and_draw_cpu_detail_text(device, font, prev_cpu, cpu, prev_cores, cores)

        i = i + 1

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32)

font = ImageFont.truetype('DejaVuSans.ttf', 12)

monitor_cpu(device, font)

#sys.stdout.write("Press ENTER to continue\n")
#sys.stdin.readline()
print("Done")
