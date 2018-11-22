import math
import random
import numpy as np
import pygame as pg
from network import NeuralNetwork
from settings import *

class Snake():
	# snake sprite class

	def __init__(self, game, neural_network):
		# snake initialisation
		self.game = game
		self.alive = True
		self.direction = random.choice([
			(1, 0),
			(-1, 0),
			(0, 1),
			(0, -1)
			])
		self.eating = False
		self.fullness = SNAKE_MAX_FULLNESS + self.game.genetic_algorithm.current_generation
		self.fitness = 0
		self.neural_network = neural_network
		self.body = []
		for i in range(SNAKE_START_LENGTH):
			self.body.append((
				SNAKE_START_X - self.direction[0],
				SNAKE_START_Y - self.direction[1]
				))
		self.food_dist = 100

	def update(self):
		# update snake
		self.consult_network()
		self.fullness -= 1
		if self.fullness <= 0:
			self.alive = False
		if not self.alive:
			self.game.genetic_algorithm.results.append({
				'network': self.neural_network,
				'fitness' : self.fitness
				})
			if self.fitness > self.game.genetic_algorithm.highscore:
				self.game.genetic_algorithm.highscore = self.fitness
		# allows the user to kill the snake
		keys = pg.key.get_pressed()
		if keys[pg.K_SPACE]:
			self.alive = False

	def draw(self):
		# draw snake on screen
		for section in self.body:
			pg.draw.rect(self.game.screen, WHITE, (
				section[0] * TILESIZE,
				section[1] * TILESIZE,
				TILESIZE,
				TILESIZE
				))
		self.draw_network(
			self.neural_network.input,
			self.neural_network.hidden,
			self.neural_network.output,
			self.neural_network.max_output
			)

	def draw_network(self, inputs, hidden, outputs, max_output):
		# input nodes
		input_nodes = []
		for i in range(INPUTS):
			input_nodes.append({
				'pos': (LAYER_IN_X, INPUT_YSTEP *(i+1)),
				'color': (0, max(50, int(255*inputs[i])), 0)
				})

		hlayer_nodes = []
		for i in range(HNODES):
			hlayer_nodes.append({
				'pos': (LAYER_H_X, HIDDEN_YSTEP *(i+1)),
				'color': (0, int(255*hidden[i]), 0)
				})

		output_nodes = []
		for i in range(OUTPUTS):
			if i == max_output:
				output_nodes.append({
					'pos': (LAYER_OUT_X, OUTPUT_YSTEP *(i+1)),
					'color': (int(255*outputs[i]), 0, 0)
					})
			else:
				output_nodes.append({
					'pos': (LAYER_OUT_X, OUTPUT_YSTEP *(i+1)),
					'color': (0, int(255*outputs[i]), 0)
					})


		for row in range(self.neural_network.weights1.shape[0]):
			for col in range(self.neural_network.weights1.shape[1]):
				color = min(255, int(self.neural_network.weights1[row,col] / self.neural_network.intensity * 255))
				pg.draw.line(
					self.game.screen,
					(color, color, color),
					input_nodes[col]['pos'],
					hlayer_nodes[row]['pos']
					)

		for row in range(self.neural_network.weights2.shape[0]):
			for col in range(self.neural_network.weights2.shape[1]):
				color = min(255, int(self.neural_network.weights2[row,col] / self.neural_network.intensity * 255))
				pg.draw.line(
					self.game.screen,
					(color, color, color),
					hlayer_nodes[col]['pos'],
					output_nodes[row]['pos']
					)

		for series in [input_nodes, hlayer_nodes, output_nodes]:
			for node in series:
				pg.draw.circle(
					self.game.screen,
					node['color'],
					node['pos'],
					16
					)



		# for xpos in [LAYER_IN_X, LAYER_H_X, LAYER_OUT_X]:
		# 	for ypos in [INPUT_YSTEP, HIDDEN_YSTEP, OUTPUT_YSTEP]:
		# 		pg.draw.circle(
		# 			self.game.screen,
		# 			GREEN,
		# 			(xpos, ypos),
		# 			TILESIZE
		# 			)

	def consult_network(self):
		# gather inputs and feed them through the snake's neural network
		inputs = []
		for i in range(5):
			inputs.append(self.check_vision(i))
		inputs.append(self.test_food_ahead())
		inputs.append(self.test_food_left())
		inputs.append(self.test_food_right())
		input_array = np.array([inputs]).T
		output = self.neural_network.feed_forward(inputs)
		if output == 0:
			self.move()
		elif output == 1:
			self.turn_anticlockwise()
		elif output == 2:
			self.turn_clockwise()

	# def consult_network(self):
	# 	# gather inputs and feed them through the snake's neural network
	# 	inputs = np.array([[
	# 			self.test_step('forward'),
	# 			self.test_step('left'),
	# 			self.test_step('right'),
	# 			self.test_food_ahead(),
	# 			self.test_food_left(),
	# 			self.test_food_right()
	# 			]]).T
	# 	output = self.neural_network.feed_forward(inputs)
	# 	if output == 0:
	# 		self.move()
	# 	elif output == 1:
	# 		self.turn_anticlockwise()
	# 	elif output == 2:
	# 		self.turn_clockwise()

	def move(self):
		# advance the snake forward one square
		new_step = tuple([sum(i) for i in zip(self.direction, self.body[0])])
		# check safeness of proposed location
		safe = self.check_coordinates(new_step)
		if not safe:
			self.alive = False
		# check for collision with food
		if new_step == self.game.food.position:
			self.game.food.alive = False
			self.eating = True
		# move body forward
		self.body.insert(0, new_step)
		if self.eating == True:
			self.fitness += 1
			self.fullness = SNAKE_MAX_FULLNESS + self.game.genetic_algorithm.current_generation
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

	def check_coordinates(self, pos):
		(x, y) = pos
		safe = True
		# check for collisions with own body
		for i in self.body:
			if i == (x, y):
				safe = False
		# check for collisions with wall
		if x < 0 or x >= MAP_WIDTH:
			safe = False
		elif y < 0 or y >= MAP_HEIGHT:
			safe = False
		# return safeness of co-ordinate
		return safe

	def check_vision(self, axis):
		# check snakes vision along an axis
		if axis == 4:
			vision_direction = (self.direction[1], -self.direction[0])
		elif axis == 3:
			temp_direction = (self.direction[1], -self.direction[0])
			vision_direction = (max(self.direction, key=abs), max(temp_direction, key=abs))
		elif axis == 2:
			vision_direction = self.direction
		elif axis == 1:
			temp_direction = (-self.direction[1], self.direction[0])
			vision_direction = (max(temp_direction, key=abs), max(self.direction, key=abs))
		elif axis == 0:
			vision_direction = (-self.direction[1], self.direction[0])
		for i in range(1, max(MAP_WIDTH, MAP_HEIGHT)):
			safe = self.check_coordinates(
				(self.body[0][0] + vision_direction[0]*i, self.body[0][1] + vision_direction[1]*i)
				)
			if not safe:
				return (max(MAP_WIDTH, MAP_HEIGHT)-i)/max(MAP_WIDTH, MAP_HEIGHT)
		return (max(MAP_WIDTH, MAP_HEIGHT)-i)/max(MAP_WIDTH, MAP_HEIGHT)

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