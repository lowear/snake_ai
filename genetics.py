"""
Genetic algorithm driver for neural network visualiser
"""


import numpy as np
from network import NeuralNetwork


class GeneticAlgorithm:
	# evolution class

	def __init__(self, game, population_size):
		# class initialisation - create first generation
		self.game = game
		self.current_generation = 1
		self.population_size = population_size
		self.population = []
		self.results = []
		for i in range(population_size):
			self.population.append(NeuralNetwork(6, 7, 3))

	def new_generation(self):
		# create new generation to test
		pass

	def simulate_generation(self):
		# simulate each snake in the generation to determine performance
		pass

	def selection(self):
		# select the snakes that pass their genes to the next generation
		pass

	def reproduction(self):
		# combine neural networks of fitest snakes from previous generation
		pass

	def mutation(self):
		# random mutations of neural networks in new generation
		pass