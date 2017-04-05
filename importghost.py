#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 13:54:52 2017

@author: thomas
"""

import telnetlib
import json
import numpy as np
import subprocess
import os
import time
import asyncio 
import multiprocessing as mp

class Ghost(object):
    def __init__(self, height, width):
        self.host = "127.0.0.1"
        self.port = 54321
        self.gamedir = "/home/thomas/Documents/Projects/ghost2/build-ghostly-Desktop_Qt_5_8_0_GCC_64bit-Debug/"
        self.gamename = "ghostly"
        self.height = 31
        self.width = 28
        self.wq = mp.Queue()
        self.rq = mp.Queue(10000)
        self.won = False

    def reset(self):
        os.chdir(self.gamedir)
        subprocess.Popen(["./"+self.gamename +" --start-at 4" + " -i 100" + " --rounds -1"], shell=True)    
        p1 = 0
        p2 = 0
        p3 = 0
        while (True):
            try:
                p1 = telnetlib.Telnet(self.host, self.port)
                p2 = telnetlib.Telnet(self.host, self.port)
                p3 = telnetlib.Telnet(self.host, self.port)
            except:
                pass
            if (p1 != 0):
                break
        time.sleep(1)
        self.connect_and_stream()
        self.msg = self.get_statemsg()
        return 
    
    async def read_msg(self):
            reader, writer = await asyncio.open_connection(self.host, self.port)
            while True:
                data = await reader.read(2500)
                if data != b"":
                        decoded = data.decode()
                        self.rq.put(decoded)
                if not self.wq.empty():
                    writer.write(self.wq.get())
    
    def f(self):
            self.loop.run_until_complete(self.read_msg())                    
    
    def connect_and_stream(self):      
        self.loop = asyncio.get_event_loop()
        mp.Process(target=self.f, args=()).start()
        
    @property
    def name(self):
        return "ghostly"
	
    @property
    def nb_actions(self):
        return 5
    
    def is_dead(self):
        dead = False
        for i, m in enumerate(self.msg):
            if "dead" in m:
                dead = True
        return dead

    def is_over(self):
        end = False
        for i, m in enumerate(self.msg):
            if "endofround" in m:
                end = True
        return end

    def is_won(self):
        won = False
        if not self.is_dead() and self.is_over():
            won = True
        return won
    
    def get_statemsg(self):
        msg = 0
        res = 0
        if self.rq.empty():
            while self.rq.empty():
                try:
                    msg = self.rq.get(True, 0.1)
                except:
                    pass
                if msg != 0:
                    break
        else:
            while res == 0:
                msg = self.rq.get()
                try:
                    res = json.loads(msg)
                    if "gamestate" not in res:
                        res = 0
                except:
                    pass
        return res

    def play(self, action):
        if action == 1:
            send = "RIGHT\n"
        if action == 2:
            send = "LEFT\n"
        if action == 3:
            send = "UP\n"
        if action == 4:
            send = "DOWN\n"
        if action == 0:
            return
        self.wq.put(send.encode())
        return
    
    def get_score(self):
        statemsg = self.get_statemsg()
        score = statemsg["gamestate"]["you"]["score"]
        return score
    
    def get_state(self):
        message = 0
        while message == 0:
            message = self.get_statemsg()
        statemsg = message["gamestate"]
        # Get binary matrix with ones where there is a wall
        def get_wall(statemsg):
            state = np.empty([self.height,self.width])
            state.dtype = int
            for i in range(len(statemsg["map"]["content"])-1, -1, -1):
                state[i] = np.array([1 if x == "|" else 0 for x in list(statemsg["map"]["content"][i])])
            return state
        # Get binary matrix with ones where there is a pellet.
        def get_pellet(statemsg):
            state = np.empty([self.height,self.width])
            state.dtype = int
            for i in range(len(statemsg["map"]["content"])-1, -1, -1):
                state[i] = np.array([1 if x == "." else 0 for x in list(statemsg["map"]["content"][i])])
            return state
        # Get binary matrix with ones where there is a superpellet.
        def get_superpellet(statemsg):
            state = np.empty([self.height,self.width])
            state.dtype = int
            for i in range(len(statemsg["map"]["content"])-1, -1, -1):
                state[i] = np.array([1 if x == "o" else 0 for x in list(statemsg["map"]["content"][i])])
            return state
        # Get binary matrix with one in own position
        def get_own(statemsg):
            state =np.zeros([self.height, self.width])
            state.dtype = int
            state[self.height-1-statemsg["you"]["x"]][self.width-1-statemsg["you"]["y"]] = 1
            return state
        # Get binary matrix with ones in position of the other players
        def get_others(statemsg):
            state =np.zeros([self.height, self.width])
            state.dtype = int
            for elem in statemsg["others"]:
                if elem["id"] in range(4):
                    state[self.height-1-elem["x"]][self.width-1-elem["y"]] = 1
            return state
        # Get binary matrix with one in the position of pacman.
        def get_pacman(statemsg):
            state =np.zeros([self.height, self.width])
            state.dtype = int
            for elem in statemsg["others"]:
                if elem["id"] == 1000:
                    state[self.height-1-elem["x"]][self.width-1-elem["y"]] = 1
            return state
        # Get binary matrix with one in own position if self is dangerous
        def get_dangerous_self(statemsg):
            state =np.zeros([self.height, self.width])
            state.dtype = int
            if statemsg["you"]["isdangerous"]==True:
                state[self.height-1-statemsg["you"]["x"]][self.width-1-statemsg["you"]["y"]] = 1
            return state
        # Get binary matrix with ones in position of other dangerous players
        def get_dangerous_others(statemsg):
            state =np.zeros([self.height, self.width])
            state.dtype = int
            for elem in statemsg["others"]:
                if elem["id"] in range(4) and elem["isdangerous"] == True:
                    state[self.height-1-elem["x"]][self.width-1-elem["y"]] = 1
            return state
        
    
        observation = np.zeros((8, self.height, self.width))
        observation.dtype = int
        observation[0] = get_wall(statemsg)
        observation[1] = get_pellet(statemsg)
        observation[2] = get_superpellet(statemsg)
        observation[3] = get_own(statemsg)
        observation[4] = get_others(statemsg)
        observation[5] = get_pacman(statemsg)
        observation[6] = get_dangerous_self(statemsg)
        observation[7] = get_dangerous_others(statemsg)
    
        #observation = np.swapaxes(observation, 0, 2)
    
        return observation
    
    def get_frame(self):
        res = self.get_state()
        return res

"""
obs = get_state(res)
wall = obs[0]
pellet = obs[1]
superpellet = obs[2]
own = obs[3]
others = obs[4]
pacman = obs[5]
dangerous_self = obs[6]
dangerous_others = obs[7]
"""

    
    
    
    
    
    
    
    
    
    
    
    
    
    