"""
Genetic algorithm driver for neural network visualiser
"""


import numpy as np
import random
from network import NeuralNetwork
from settings import *


class GeneticAlgorithm:
	# evolution class

	def __init__(self, game, population_size):
		# class initialisation - create first generation
		self.game = game
		self.current_generation = 1
		self.population_size = population_size
		self.population = []
		self.results = []
		self.inputs = INPUTS
		self.hidden_nodes = HIDDEN_NODES
		self.outputs = OUTPUTS
		for i in range(population_size):
			self.population.append(
				NeuralNetwork(
					self.inputs,
					self.hidden_nodes,
					self.outputs
					)
				)

	def new_generation(self):
		# create new generation to test
		pass

	def simulate_generation(self):
		# simulate each snake in the generation to determine performance
		pass

	def selection(self):
		# select the snakes that pass their genes to the next generation
		# sort current population by fitness
		self.results = sorted(
			self.results, key=lambda k: k['fitness'], reverse = True
			)
		# retain only elite proportion of current generation
		elite_qty = int(self.population_size * ELITISM)
		self.results = self.results[:elite_qty]
		for result in self.results:
			print(result['fitness'])

	def reproduction(self):
		# combine neural networks of fitest snakes from previous generation
		self.new_population = []
		for network in self.results:
			partner = random.choice(self.results)
			# create weights1 array for new snake
			new_weights1 = np.zeros(
				(
					network['weights1'].shape[0],
					network['weights1'].shape[1]
					)
				)
			for row in range(new_weights1.shape[0]):
				for col in range(new_weights1.shape[1]):
					gene1 = network['weights1'][row,col]
					gene2 = partner['weights1'][row,col]
					new_weights1[row,col] = random.choice([gene1, gene2])
			# create weights2 array for new snake
			new_weights2 = np.zeros(
				(
					network['weights2'].shape[0],
					network['weights2'].shape[1]
					)
				)
			for row in range(new_weights2.shape[0]):
				for col in range(new_weights2.shape[1]):
					gene1 = network['weights2'][row,col]
					gene2 = partner['weights2'][row,col]
					new_weights2[row,col] = random.choice([gene1, gene2])
			# create new neural network for new population
			self.new_population.append(
				NeuralNetwork(
					self.inputs,
					self.hidden_nodes,
					self.outputs
					)
				)
			self.new_population[-1].weights1 = new_weights1
			self.new_population[-1].weights2 = new_weights2
		self.population = self.new_population

	def mutation(self):
		# random mutations of neural networks in new generation
		pass