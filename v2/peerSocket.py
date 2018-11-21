#!/usr/bin/env python3
import asyncio
import websockets
import json

class PeerSocket(object):
    """Handles socket incoming and outgoing messages"""

    def __init__(self, port, message_handler):
        self.port = port
        self.message_handler = message_handler

    async def server(self, websocket, path):
        data = await websocket.recv()
        await self.message_handler(data)

    async def send(self, destination, message):
        json_message = json.dumps(message)
        print(json_message)
        async with websockets.connect(destination) as websocket:
            await websocket.send(json_message)

    def start_server(self):
        # Thread does not have its own event loop, create one
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(self.server, 'localhost', self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        # Run the server forever
        asyncio.get_event_loop().run_forever()
