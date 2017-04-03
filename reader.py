#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 12:43:47 2017

@author: thomas
"""

import asyncio 
import telnetlib
import json 
import subprocess

import queue


host = "127.0.0.1"
port = 54321
lq = queue.LifoQueue()

async def read_msg():
    reader, writer = await asyncio.open_connection(host, port)

    while True:
        data = await reader.read(2800)
        if data != b"":
            decoded = data.decode()
            #msgs = decoded.split("\n{\"gamestate\"")
            print(decoded)
            lq.put_nowait(decoded)
            #for msg in msgs:
            #    if msg.startswith(":{\"map\":"):
            #        rq.put_nowait(msg)
            #        return

def call_in_background(target, *, loop=None, executor=None):
    """Schedules and starts target callable as a background task

    If not given, *loop* defaults to the current thread's event loop
    If not given, *executor* defaults to the loop's default executor

    Returns the scheduled task.
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    if callable(target):
        return loop.run_in_executor(executor, target)
    raise TypeError("target must be a callable, "
                    "not {!r}".format(type(target)))
    

test = call_in_background(read_msg)