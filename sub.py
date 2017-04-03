#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 12:39:30 2017

@author: thomas
"""
import subprocess
import telnetlib
import os
import time
import asyncio

host = "127.0.0.1"
port = 54321
gamedir = "/home/thomas/Documents/Projects/ghost2/build-ghostly-Desktop_Qt_5_8_0_GCC_64bit-Debug/"
pydir = "/home/thomas/Documents/Projects/ghost/"
gamename = "ghostly"
height = 31
width = 28

os.chdir(gamedir)
subprocess.Popen(["./"+gamename +" --start-at 4" + " -i 100" + " --rounds -1"], shell=True)    
time.sleep(1)
p1 = telnetlib.Telnet(host, port)
p2 = telnetlib.Telnet(host, port)
p3 = telnetlib.Telnet(host, port)

os.chdir(pydir)

async def start_reader():
    # start child process
    p = await asyncio.create_subprocess_exec(["python reader.py"] stdout=PIPE)
    
loop = asyncio.get_event_loop()    



t = lq.get_nowait()