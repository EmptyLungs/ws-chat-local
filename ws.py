import uuid

from aiohttp import web, WSMsgType


class ChatSock(web.View):
    ws_name = None

    async def broadcast(self, message):
        for conn_name, conn in self.request.app.ws_connections.items():
            if conn_name != self.ws_name:
                await conn.send_str(message)

    async def get(self):
        app = self.request.app
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        username = self.request.query.get('username', str(uuid.uuid4()))
        self.ws_name = username
        if username in app.ws_connections.keys():
            return web.HTTPBadRequest()

        app.ws_connections[username] = ws
        join_message = f"{username} влетел в хату"
        await self.broadcast(join_message)
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await self.broadcast(f"{self.ws_name} ливнул из чата")
                    await ws.close()
                    del app[self.ws_name]
                else:
                    text = msg.data.strip()
                    await self.broadcast(f"{username}: {text}")
            elif (msg.type == WSMsgType.ERROR):
                app.logger.dubg('ws connection error: {}'.format(ws.exception()))
        return ws
