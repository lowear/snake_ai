import random
import pygame as pg
from settings import *

unicorn = pg.image.load('unicorn.png')
dinosaur = pg.image.load('dinosaur.png')

class Food():
	# food object

	def __init__(self, game):
		# food initialisation
		self.game = game
		self.alive = True
		self.position = self.get_position()
		self.image = random.choice([unicorn, dinosaur])

	def update(self):
		# update food object
		if not self.alive:
			self.game.food = Food(self.game)
			if self.image == unicorn:
				self.game.genetic_algorithm.unicorns += 1
			else:
				self.game.genetic_algorithm.dinosaurs += 1

	def draw(self):
		# draw food object on screen
		self.game.screen.blit(self.image, (
			(self.position[0]*TILESIZE) - 8,
			(self.position[1]*TILESIZE) - 8,
			))
		# pg.draw.rect(self.game.screen, RED, (
		# 	self.position[0] * TILESIZE,
		# 	self.position[1] * TILESIZE,
		# 	TILESIZE,
		# 	TILESIZE
		# 	))

	def get_position(self):
		# find position where food will be placed
		while True:
			position = (
				random.randint(0, MAP_WIDTH - 1),
				random.randint(0, MAP_HEIGHT - 1)
				)
			if position not in self.game.snake.body:
				return position