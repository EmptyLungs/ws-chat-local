import asyncio

from aiohttp.web_urldispatcher import UrlDispatcher
from aiohttp import web

from ws import ChatSock

loop = asyncio.get_event_loop()
router = UrlDispatcher()
router.add_get('/ws', ChatSock)
app = web.Application(router=router, middlewares=[])
app.ws_connections = {}
web.run_app(app, host='0.0.0.0', port=8001)
