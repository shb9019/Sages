"""Network Object unique for every contest to maintain connection with every other peer"""
#!/usr/bin/env python3
import time
from json import loads
from urllib.request import urlopen
from peerSocket import PeerSocket
from handlers.sage import Sage
from handlers.contest import Contest
from wallet import Wallet
import asyncio
import threading


class Network:
    """Network Class"""

    def __init__(self, port):
        self.peers = []
        self.port = port
        self.address = 'ws://localhost:' + str(self.port)
        self.peersocket = PeerSocket(self.port, self.message_handler)
        self.sage_handler = Sage(self.address, self.peersocket)
        self.contest_handler = Contest()
        self.wallet = Wallet()
        self.wallet.generate_keys()
        threading.Thread(target=self.peersocket.start_server).start()


    async def message_handler(self, message):
        """Handle incoming messages"""
        if message["code"] == 1:
            print("Received Heartbeat")
        elif message["code"] == 2:
            print("Received Heartbeat Echo")
        elif message["code"] == 6:
            await self.sage_handler.handle_sage_request(message["source_address"])
        elif message["code"] == 7:
            if message["success"] == True:
                self.sage_handler.accept_sage(message["sages"])
            else:
                self.sage_handler.reject_sage()
