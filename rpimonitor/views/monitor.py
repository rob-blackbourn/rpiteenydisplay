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
        self.stats = None
        self.prev_stats = None
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial, width=128, height=32)
        self.font = ImageFont.truetype('DejaVuSans.ttf', 12)        
        app.on_startup.append(self.on_startup)
        app.on_cleanup.append(self.on_cleanup)

    def render(self):
        """Render the status"""
        calc_and_draw_cpu_detail_text(
            self.device, self.font, 
            self.prev_stats.cpu, self.stats.cpu,
            self.prev_stats.cores, self.stats.cores)
        
    async def poll(self):
        """Poll the status"""
        self.stats = await Stat.sample_async()
        try:
            while self.is_monitoring:
                print("Monitoring")
                await asyncio.sleep(self.poll_seconds)

                self.prev_stats = self.stats
                self.stats = await Stat.sample_async()
                self.render()

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
