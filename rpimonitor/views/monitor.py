"""The main monitor class"""

import asyncio
from aiohttp import web
import aiohttp_jinja2

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import ImageFont

from rpimonitor.monitor.stat import Stat
from rpimonitor.display.cpu_detail import draw_cpu_detail_text

class Monitor(object):
    """Integrates with aiohttp to provide a polling background monitor"""

    def __init__(self, app, poll_seconds=1):
        self.is_monitoring = True
        self.poll_seconds = poll_seconds
        self.background_task = None
        self.stat = None
        self.prev_stat = None
        self.condition = asyncio.Condition()
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial, width=128, height=32)
        self.font = ImageFont.truetype('DejaVuSans.ttf', 12)        
        app.on_startup.append(self.on_startup)
        app.on_cleanup.append(self.on_cleanup)

    def render(self):
        """Render the status"""
        draw_cpu_detail_text(self.device, self.font, self.cpu_usage, self.core_usages)
        
    async def poll(self):
        """Poll the status"""
        self.stat = await Stat.sample_async()
        try:
            while self.is_monitoring:
                print("Monitoring")
                await asyncio.sleep(self.poll_seconds)

                self.prev_stat = self.stat
                self.stat = await Stat.sample_async()
                with await self.condition:
                    self.condition.notify_all()
                self.render()

        except asyncio.CancelledError:
            pass
        except Exception as error:
            print(error)
        
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

    @property
    def cpu_usage(self):
        return (self.stat.cpu - self.prev_stat.cpu).usage

    @property
    def core_usages(self):
        return [(self.stat.cores[key] - self.prev_stat.cores[key]).usage for key in self.stat.cores.keys()]

@aiohttp_jinja2.template('index.html')
async def index(request):
    """The index page"""
    return {}

async def index_ws(request):
    """The index page"""
    monitor = request.app['monitor']

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while not ws.closed:
        print("Acquiring")
        with await monitor.condition:
            print("Waiting")
            await monitor.condition.wait()
            print("Received")
            cpu_usage = 100 * monitor.cpu_usage
            core_usages = [100 * usage for usage in monitor.core_usages]
            data = {'cpu_usage': cpu_usage, 'core_usages': core_usages}
            await ws.send_json(data)

    print('websocket connection closed')

    return ws