"""
game class for neural network visualiser
"""

import sys
import pygame as pg
from food import Food
from genetics import GeneticAlgorithm
from network import NeuralNetwork, sigmoid, sigmoid_derivative
from settings import *
from snake import Snake


class Game:
	# session instance class

	def __init__(self):
		# class initialisation
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.gen = 1
		self.fps = FPS

	def new_simulation(self):
		# start a new simulation
		self.genetic_algorithm = GeneticAlgorithm(self, POPULATION_SIZE)
		while True:
			for nerual_network in self.genetic_algorithm.population:
				self.new_game(nerual_network)
			self.genetic_algorithm.selection()
			self.genetic_algorithm.reproduction()
			print('next gen')
			self.gen += 1

	def new_game(self, neural_network):
		# start new game with a new snake
		self.all_sprites = pg.sprite.Group()
		self.food = Food(self)
		self.snake = Snake(self, 10, 10, 3, neural_network)
		self.run()

	def run(self):
		# game loop
		while self.snake.alive:
			self.dt = self.clock.tick(self.fps) / 1000
			self.events()
			self.update()
			if self.gen >= 100:
				self.fps = 60
				self.draw()

	def update(self):
		# game loop update
		self.all_sprites.update()

	def events(self):
		# execute game events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					pg.quit()
					sys.exit()

	def draw(self):
		# draw on screen elements:
		self.screen.fill(BLACK)
		self.draw_grid()
		for sprite in self.all_sprites:
			sprite.draw()
		pg.display.flip()

	def draw_grid(self):
		# draw map tile grid
		for x in range(0, WIDTH, TILESIZE):
			pg.draw.line(self.screen, GREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pg.draw.line(self.screen, GREY, (0, y), (WIDTH, y))

	def show_start_screen(self):
		pass