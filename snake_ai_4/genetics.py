import numpy as np
import random
from network import NeuralNetwork
from settings import *


class GeneticAlgorithm:
	# evolution class

	def __init__(self, game):
		# class initialisation - create first generation
		self.game = game
		self.current_generation = 1
		self.results = []
		self.population = []
		self.highscore = 0
		self.dinosaurs = 0
		self.unicorns = 0
		self.cur_snake = 0
		for i in range(POPULATION_SIZE):
			self.population.append(NeuralNetwork())

	def selection(self):
		# select fittest snakes from current generation
		self.results = sorted(
			self.results, key=lambda k: k['fitness'], reverse = True
			)
		self.results = self.results[:ELITE_QTY]

	def reproduction(self):
		# combine neural networks of fittest snakes from previous gen
		self.population = []

		for result in self.results[:10]:
			self.population.append(
				NeuralNetwork(
					result['network'].weights1,
					result['network'].weights2
					)
				)

		for i in range(2):
			self.population.append(NeuralNetwork())

		max_capacity = False
		while not max_capacity:
			for parent in self.results:

				if len(self.population) >= POPULATION_SIZE:
					max_capacity = True
					break

				partner = random.choice(self.results)

				# create weights1 array for new snake
				new_weights1 = np.zeros(
					(
						parent['network'].weights1.shape[0],
						parent['network'].weights1.shape[1]
						)
					)
				for row in range(new_weights1.shape[0]):
					for col in range(new_weights1.shape[1]):
						gene1 = parent['network'].weights1[row,col]
						gene2 = partner['network'].weights1[row,col]
						new_weights1[row,col] = random.choice([gene1, gene2])

				# create weights2 array for new snake
				new_weights2 = np.zeros(
					(
						parent['network'].weights2.shape[0],
						parent['network'].weights2.shape[1]
						)
					)
				for row in range(new_weights2.shape[0]):
					for col in range(new_weights2.shape[1]):
						gene1 = parent['network'].weights2[row,col]
						gene2 = partner['network'].weights2[row,col]
						new_weights2[row,col] = random.choice([gene1, gene2])

				# create child neural network for new population
				self.population.append(
					NeuralNetwork(
						new_weights1,
						new_weights2,
						)
					)
		for result in self.results:
			print(result['fitness'])
		self.results = []

	def mutation(self):
		# randomly mutate new population
		num_mutations = int(len(self.population) * MUTATION_RATE)
		for i in range(num_mutations):
			network = random.randint(0, len(self.population) - 1)
			option = random.choice([0, 1])
			if option == 0:
				row = random.randint(0, self.population[network].weights1.shape[0]-1)
				col = random.randint(0, self.population[network].weights1.shape[1]-1)
				self.population[network].weights1[row][col] *= random.uniform(0.5, 1.5)
			else:
				row = random.randint(0, self.population[network].weights2.shape[0]-1)
				col = random.randint(0, self.population[network].weights2.shape[1]-1)
				self.population[network].weights2[row][col] *= random.uniform(0.5, 1.5)