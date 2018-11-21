"""Network Object unique for every contest to maintain connection with every other peer"""
#!/usr/bin/env python3
import time
from json import loads
from urllib.request import urlopen
from peerSocket import PeerSocket
import asyncio
import threading

class Network:
    """Network Class"""
    def __init__(self, sages, port):
        self.sages = sages # List of Sage IP Addresses and their Public Keys
        self.peers = sages # List of all peers in network, initially same as sages
        self.port = port # Current Node Port
        # Socket Object handles all communication
        self.peersocket = PeerSocket(self.port, self.message_handler)
        self.address = 'ws://localhost:' + str(self.port) # Web Socket address of the node
        # Start Websocket Server in a seperate thread
        threading.Thread(target=self.peersocket.start_server).start()

    def get_register_details(self, verifying_key):
        """Send verifying key and ip address to get registration details"""
        register_message = {}
        register_message.verifying_key = verifying_key
        register_message.ip_address = self.ip_address
        register_message.timestamp = round(time.time())
        destination_list = self.peers
        return (register_message, destination_list)

    def add_peers(self, peers):
        """Add a peer to the list"""
        self.peers.append(peers)

    def update_sages(self, sages):
        """Update the existing list of sages"""
        self.sages = sages

    async def message_handler(self, json_message):
        """Handle incoming messages"""
        message = loads(json_message)
        if message["code"] == 1:
            await self.send_heartbeat_echo(message["sender"])
        elif message["code"] == 2:
            print("Received Heartbeat Echo")

    async def send_heartbeat_echo(self, sender):
        """Send Heartbeat Echo to sender of Heartbeat message"""
        message = {}
        message["code"] = 2
        message["sender"] = self.address
        print("Heartbeat Echo Sent")
        await self.peersocket.send(sender, message)

    def send_heartbeat(self, address):
        """Send Heartbeat to address"""
        message = {}
        message['code'] = 1
        message['sender'] = self.address
        print("Sending Heartbeat")
        asyncio.run(self.peersocket.send(address, message))

    def register_sage(self):
        """Register this node as sage"""
        self.sages = []
        self.peers = []
        self.sages.push(self.address)

    