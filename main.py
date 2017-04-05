#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 09:17:08 2017

@author: thomas
"""

from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import sgd
from importghost import Ghost
from agent import Agent
import random


nb_frames = 1
state_mats = 8
height = 31
width = 28
hidden_size = 100

model = Sequential()
model.add(Flatten(input_shape=(nb_frames, state_mats, height, width)))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(5))
model.compile(sgd(lr=.2), "mse")

game = Ghost(height, width)
agent = Agent(model)

game.reset()

for i in range(1000):
    S = game.get_state()
    game.play(random.randrange(0,4,1))


agent.train(game)



m = game.get_state()

agent.play(game)
