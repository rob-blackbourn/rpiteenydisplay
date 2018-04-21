import time
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

from rpimonitor.monitor.stat import Stat
from rpimonitor.display.cpu_detail import calc_and_draw_cpu_detail_text, draw_signal_strength_graph

def monitor_cpu(device, font, count=100):
    """Monitor the cpu"""
    stats = Stat.sample()
    cpu, cores = stats.cpu, stats.cores
    i = 0
    while i < count:

        time.sleep(1)

        prev_cpu, prev_cores = cpu, cores

        stats = Stat.sample()
        cpu, cores = stats.cpu, stats.cores
        calc_and_draw_cpu_detail_text(device, font, prev_cpu, cpu, prev_cores, cores)

        i = i + 1

def monitor_cpu2(device, count=100):
    """Monitor the cpu"""
    stats = Stat.sample()
    cpu, cores = stats.cpu, stats.cores
    i = 0
    while i < count:

        time.sleep(1)

        prev_cpu, prev_cores = cpu, cores

        stats = Stat.sample()
        cpu, cores = stats.cpu, stats.cores
        draw_signal_strength_graph(device, (5,5), (cpu - prev_cpu).usage)

        i = i + 1

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32)

font = ImageFont.truetype('DejaVuSans.ttf', 12)

#draw_signal_strength_graph(device, (0, 0), 0.0, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.1, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.2, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.3, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.4, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.5, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.6, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.7, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.8, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 0.9, 5, (4,4))
#draw_signal_strength_graph(device, (0, 0), 1.0, 5, (4,4))
monitor_cpu(device, font)
#monitor_cpu2(device)

#sys.stdout.write("Press ENTER to continue\n")
#sys.stdin.readline()
print("Done")
