import numpy as np
from settings import *


class NeuralNetwork:
	# two-hidden-layer neural network class

	@classmethod
	def sigmoid(cls, x):
		# return the sigmoid function of x
		return 1 / (1 + np.exp(-x))

	def __init__(self, weights1=False, weights2=False):
		# neural network initialisation
		self.weights1 = weights1
		self.weights2 = weights2
		# if no weights, generate new neural network
		if isinstance(self.weights1, bool):
			self.weights1 = np.random.rand(HNODES, INPUTS)
			self.weights2 = np.random.rand(OUTPUTS, HNODES)
		self.intensity = max(np.amax(self.weights1), np.amax(self.weights2))

	def feed_forward(self, inputs):
		# process inputs through the network
		layer1 = NeuralNetwork.sigmoid(np.dot(self.weights1, inputs))
		output = NeuralNetwork.sigmoid(np.dot(self.weights2, layer1))
		self.input = inputs
		self.hidden = layer1
		self.output = output
		self.max_output = np.argmax(output)
		# return the index of highest valued output node
		return np.argmax(output)