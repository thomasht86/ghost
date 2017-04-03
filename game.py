#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 06:54:57 2017

@author: thomas
"""

class Game(object):
	
	def __init__(self):
		self.reset()

	@property
	def name(self):
		return "ghostly"
	
	@property
	def nb_actions(self):
		return 5
	
	def reset(self):
		pass

	def play(self, action):
		pass

	def get_state(self):
		return None

	def get_score(self):
		return 0

	def is_over(self):
		return False

	def is_won(self):
		return False

	def get_frame(self):
		return self.get_state()

	def draw(self):
		return self.get_state()

	def get_possible_actions(self):
		return range(self.nb_actions)