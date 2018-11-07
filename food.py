"""
food class for neural network visualiser
"""

from random import randint
import pygame as pg
from settings import *


class Food(pg.sprite.Sprite):
	# food object

	def __init__(self, game):
		# class initialisation
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.alive = True
		self.position = [randint(0, MAP_WIDTH-1), randint(0, MAP_HEIGHT-1)]

	def update(self):
		if not self.alive:
			self.kill()
			self.game.food = Food(self.game)

	def draw(self):
		pg.draw.rect(self.game.screen, RED, (
			self.position[0] * TILESIZE,
			self.position[1] * TILESIZE,
			TILESIZE,
			TILESIZE
			))