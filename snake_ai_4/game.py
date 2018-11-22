import sys
import pygame as pg
from settings import *
from genetics import GeneticAlgorithm
from snake import Snake
from food import Food

class Game:
	# session class

	def __init__(self):
		# session initialisation
		pg.init()
		pg.font.init()
		self.font = pg.font.SysFont('Arial', 16)
		self.screen = pg.display.set_mode(
			(TOTAL_WIDTH, GRID_HEIGHT)
			)
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.fps = FPS
		self.render = True

	def new_simulation(self):
		# start a new simulation session
		self.genetic_algorithm = GeneticAlgorithm(self)
		while True:
			self.genetic_algorithm.cur_snake = 0
			for network in self.genetic_algorithm.population:
				self.new_game(network)
				self.genetic_algorithm.cur_snake += 1
			self.genetic_algorithm.selection()
			self.genetic_algorithm.reproduction()
			self.genetic_algorithm.mutation()
			self.genetic_algorithm.current_generation += 1
			print('Generation: ', self.genetic_algorithm.current_generation)

	def new_game(self, neural_network):
		# start a new game of snake with the specified neural network
		self.snake = Snake(self, neural_network)
		self.food = Food(self)
		self.run()

	def run(self):
		# game loop
		while self.snake.alive:
			self.events()
			self.update()
			if self.render:
				self.draw()
				self.clock.tick(self.fps) / 1000

	def update(self):
		# game loop update
		self.snake.update()
		self.food.update()

	def events(self):
		# check for user interaction events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					self.render = True
					self.fps *= 2
				elif event.key == pg.K_DOWN:
					self.render = True
					self.fps = int(self.fps/2)
				if self.fps < 1:
					self.fps = 1
				elif self.fps > 128:
					self.render = False
					self.fps = 128


	def draw(self):
		# draw on screen elements
		self.screen.fill(BLACK)
		self.draw_grid()
		self.snake.draw()
		self.food.draw()

		genstring = 'Generation: ' + str(self.genetic_algorithm.current_generation)
		gentext = self.font.render(genstring, False, WHITE)
		self.screen.blit(gentext,(TOTAL_WIDTH - gentext.get_width(), (GRID_HEIGHT - 3*gentext.get_height())))

		snakestring = 'Snake: ' + str(self.genetic_algorithm.cur_snake)
		snaketext = self.font.render(snakestring, False, WHITE)
		self.screen.blit(snaketext,(TOTAL_WIDTH - snaketext.get_width(), (GRID_HEIGHT - 2*snaketext.get_height())))

		scorestring = 'Highscore: ' + str(self.genetic_algorithm.highscore)
		scoretext = self.font.render(scorestring, False, WHITE)
		self.screen.blit(scoretext,(TOTAL_WIDTH - scoretext.get_width(), (GRID_HEIGHT - 1*scoretext.get_height())))
		pg.display.flip()

	def draw_grid(self):
		# draw map tile grid
		for x in range(0, GRID_WIDTH  + 1, TILESIZE):
			pg.draw.line(self.screen, GREY, (x, 0), (x, GRID_HEIGHT))
		for y in range(0, GRID_HEIGHT, TILESIZE):
			pg.draw.line(self.screen, GREY, (0, y), (GRID_WIDTH, y))