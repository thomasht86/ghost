#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 06:50:50 2017

@author: thomas
"""
import asyncio 
import telnetlib
import json 
import subprocess
import os
import time
import queue

class Reader:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 54321
        self.lq = queue.LifoQueue()

    async def read_msg(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        lq = self.lq
        while True:
            data = await reader.read(2800)
            if data != b"":
                decoded = data.decode()
                #msgs = decoded.split("\n{\"gamestate\"")
                lq.put_nowait(decoded)
                #for msg in msgs:
                #    if msg.startswith(":{\"map\":"):
                #        rq.put_nowait(msg)
                #        return
    
    def start_reader(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(read_msg())
