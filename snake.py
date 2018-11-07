"""
snake class for neural network visualiser
"""

import numpy as np
import pygame as pg
from network import NeuralNetwork
from settings import *


class Snake(pg.sprite.Sprite):
	# player object

	def __init__(self, game, x, y, length, neural_network):
		# class initialisation
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.alive = True
		self.direction = [1, 0]
		self.body = []
		for i in range(0, length):
			self.body.append([x - i, y])
		self.eating = False
		self.fullness = 1000
		self.fitness = 0

		self.neural_network = neural_network

	def update(self):
		# update snake
		self.user_kill()
		self.consult_network()
		self.fullness -= 1
		if self.fullness <= 0:
			self.alive = False
		if not self.alive:
			self.game.genetic_algorithm.results.append({
				'weights1': self.neural_network.weights1,
				'weights2': self.neural_network.weights2,
				'fitness': self.fitness
				})
			self.kill()

	def draw(self):
		# draw snake on screen
		for section in self.body:
			pg.draw.rect(self.game.screen, WHITE, (
				section[0] * TILESIZE,
				section[1] * TILESIZE,
				TILESIZE,
				TILESIZE
				))

	def consult_network(self):
		# gather inputs and feed them through the snake's neural network
		inputs = np.array([[
				self.test_step('forward'),
				self.test_step('left'),
				self.test_step('right'),
				self.test_food_ahead(),
				self.test_food_left(),
				self.test_food_right()
				]]).T
		output = self.neural_network.feed_forward(inputs)
		if output == 0:
			self.move()
		elif output == 1:
			self.turn_anticlockwise()
		elif output == 2:
			self.turn_clockwise()

	def test_step(self, direction):
		# check to see if proposed move is safe
		if direction == 'forward':
			test_direction = self.direction
		elif direction == 'left':
			test_direction = [self.direction[1], -self.direction[0]]
		elif direction == 'right':
			test_direction = [-self.direction[1], self.direction[0]]
		test_step = [sum(i) for i in zip(test_direction, self.body[0])]
		# check for collisions with own body
		for i in self.body:
			if i == test_step:
				return 0
		# check for collisions with wall
		if test_step[0] < 0 or test_step[0] >= MAP_WIDTH:
			return 0
		elif test_step[1] < 0 or test_step[1] >= MAP_HEIGHT:
			return 0
		# move is safe
		return 1

	def test_food_ahead(self):
		# find food location relative to snake's head
		if self.direction[0] == 1: # moving right
			if self.game.food.position[0] > self.body[0][0]:
				return 1
		elif self.direction[0] == -1: # movig left
			if self.game.food.position[0] < self.body[0][0]:
				return 1
		elif self.direction[1] == 1: # moving down
			if self.game.food.position[1] > self.body[0][1]:
				return 1
		elif self.direction[1] == -1: # moving up
			if self.game.food.position[1] < self.body[0][1]:
				return 1
		return 0

	def test_food_right(self):
		# find food location relative to snake's head
		if self.direction[0] == 1: # moving right
			if self.game.food.position[1] > self.body[0][1]:
				return 1
		elif self.direction[0] == -1: # movig left
			if self.game.food.position[1] < self.body[0][1]:
				return 1
		elif self.direction[1] == 1: # moving down
			if self.game.food.position[0] < self.body[0][0]:
				return 1
		elif self.direction[1] == -1: # moving up
			if self.game.food.position[0] > self.body[0][0]:
				return 1
		return 0

	def test_food_left(self):
		# find food location relative to snake's head
		if self.direction[0] == 1: # moving right
			if self.game.food.position[1] < self.body[0][1]:
				return 1
		elif self.direction[0] == -1: # movig left
			if self.game.food.position[1] > self.body[0][1]:
				return 1
		elif self.direction[1] == 1: # moving down
			if self.game.food.position[0] > self.body[0][0]:
				return 1
		elif self.direction[1] == -1: # moving up
			if self.game.food.position[0] < self.body[0][0]:
				return 1
		return 0

	def move(self):
		# advance the snake forward one square
		new_step = [sum(i) for i in zip(self.direction, self.body[0])]
		# check for collisions with own body
		for i in self.body:
			if i == new_step:
				self.alive = False
		# check for collisions with wall
		if new_step[0] < 0 or new_step[0] >= MAP_WIDTH:
			self.alive = False
		elif new_step[1] < 0 or new_step[1] >= MAP_HEIGHT:
			self.alive = False
		# check for collision with food
		if new_step == self.game.food.position:
			self.game.food.alive = False
			self.eating = True
		# move body forward
		self.body.insert(0, new_step)
		if self.eating == True:
			self.fitness += 1
			self.fullness = 1000
			self.eating = False
		else:
			self.body.pop()

	def turn_clockwise(self):
		# advance the snake one square to the right
		self.direction = [-self.direction[1], self.direction[0]]
		self.move()

	def turn_anticlockwise(self):
		# advance the snake one squareto the left
		self.direction = [self.direction[1], -self.direction[0]]
		self.move()

	def get_keys(self):
		# check for player inputs and move accordingly
		keys = pg.key.get_pressed()
		if keys[pg.K_w]:
			self.move()
		elif keys[pg.K_a]:
			self.turn_anticlockwise()
		elif keys[pg.K_d]:
			self.turn_clockwise()

	def user_kill(self):
		# allows the user to kill the snake
		keys = pg.key.get_pressed()
		if keys[pg.K_SPACE]:
			self.alive = False