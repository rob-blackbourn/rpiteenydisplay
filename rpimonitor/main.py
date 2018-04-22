"""Web server"""

import os.path
import asyncio
from aiohttp import web
import jinja2
import aiohttp_jinja2

from rpimonitor.views.monitor import Monitor, index, index_ws

PROJECT_ROOT = os.path.dirname(__file__)

def main(args):
    """Run the web server"""
    app = web.Application()
    app.router.add_static('/node_modules/', path=os.path.join(PROJECT_ROOT, 'node_modules'), name='node_modules')
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('rpimonitor', 'templates'))
    app.router.add_get('/', index)
    app.router.add_get('/ws', index_ws)
    app['monitor'] = Monitor(app)
    web.run_app(app, host='127.0.0.1', port=8080)