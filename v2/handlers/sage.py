"""Class to handle all Sage activities"""
#!/usr/bin/env python3
import asyncio

class Sage:

    def __init__(self, address, peersocket):
        self.sages = []
        self.address = address
        self.is_sage = False
        self.peersocket = peersocket
        self.state = "IDLE"
        self.sage_limit = 5


    def add_sages(self, sages):
        self.sages.append(sages)


    def clear_sages(self, sages):
        self.sages.clear()


    def set_is_sage(self, is_sage):
        self.is_sage = is_sage


    def create_contest(self):
        self.is_sage = True
        self.state = "SAGE"
        self.sages.clear()
        self.sages.append(self.address)


    def request_sage(self, destination):
        if self.state == "IDLE":
            message = {}
            message["source_address"] = self.address
            message["destination_address"] = destination
            message["code"] = 6
            self.state = "SAGE_REQ_SENT"
            asyncio.run(self.peersocket.send(destination,message))


    def accept_sage(self, sages):
        if self.state == "SAGE_REQ_SENT":
            self.state = "SAGE"
            self.is_sage = True
            self.sages = sages
        elif self.state == "SAGE":
            self.sages = sages


    def reject_sage(self):
        if self.state == "SAGE_REQ_SENT" or self.state == "SAGE":
            self.state = "IDLE"
            self.is_sage = False
            self.sages.clear()


    async def update_all_sages(self):
        message = {}
        message["source_address"] = self.address
        message["code"] = 7
        message["type"] = 4
        message["success"] = True
        message["sages"] = self.sages

        for destination in self.sages:
            message["destination_address"] = destination
            await self.peersocket.send(destination, message)


    async def handle_sage_request(self, address):
        message = {}
        message["source_address"] = self.address
        message["destination_address"] = address
        message["code"] = 7

        if self.state == "SAGE":

            if address in self.sages:
                message["type"] = 4
                message["success"] = True
                message["sages"] = self.sages

            elif self.sage_limit <= len(self.sages):
                message["type"] = 7
                message["success"] = False
                message["sages"] = []

            else:
                message["type"] = 1
                message["success"] = True
                message["sages"] = self.sages
                self.add_sages(address)

        else:
            message["type"] = 13
            message["success"] = False
            message["sages"] = []
        await self.peersocket.send(address, message)

        await self.update_all_sages()


    def deregister_sage(self):
        self.sages.remove(self.address)
        self.update_all_sages()