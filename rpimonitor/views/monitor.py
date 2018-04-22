"""The main monitor class"""

import asyncio
import time

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

from rpimonitor.monitor.stat import Stat
from rpimonitor.display.cpu_detail import calc_and_draw_cpu_detail_text

class Monitor(object):
    """Integrates with aiohttp to provide a polling background monitor"""

    def __init__(self, app, poll_seconds=1):
        self.is_monitoring = True
        self.poll_seconds = poll_seconds
        self.background_task = None
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial, width=128, height=32)
        self.font = ImageFont.truetype('DejaVuSans.ttf', 12)        
        app.on_startup.append(self.on_startup)
        app.on_cleanup.append(self.on_cleanup)

    def render(self, prev_cpu, cpu, prev_cores, cores):
        calc_and_draw_cpu_detail_text(self.device, self.font, prev_cpu, cpu, prev_cores, cores)
        
    async def poll(self):
        """Poll the status"""
        stats = await Stat.sample_async()
        cpu, cores = stats.cpu, stats.cores        
        try:
            while self.is_monitoring:
                print("Monitoring")
                await asyncio.sleep(self.poll_seconds)

                prev_cpu, prev_cores = cpu, cores
                stats = await Stat.sample_async()
                cpu, cores = stats.cpu, stats.cores
                calc_and_draw_cpu_detail_text(self.device, self.font, prev_cpu, cpu, prev_cores, cores)

        except asyncio.CancelledError:
            pass
        
    async def on_startup(self, app):
        """Start monitoring the system state"""
        self.background_task = app.loop.create_task(self.poll())

    async def on_cleanup(self, app):
        """Stop monitoring the system state"""
        print("Stop monitoring")
        self.is_monitoring = False
        try:
            self.background_task.cancel()
        except Exception as error:
            print(error)
