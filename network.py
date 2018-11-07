"""
neural network class and supporting functions for neural network visualiser
"""

import numpy as np


def sigmoid(x):
	# return the sigmoid function of x
	return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
	# return derivative of sigmoid function
	return x * (1 - x)


class NeuralNetwork:
	# single-hidden-layer neural network class

	def __init__(self, qty_inputs, qty_hlayer_nodes, qty_outputs):
		# initiate neural network with one hidden layer
		self.qty_inputs = qty_inputs
		self.qty_hlayer_nodes = qty_hlayer_nodes
		self.qty_outputs = qty_outputs
		self.weights1 = np.random.rand(qty_hlayer_nodes, qty_inputs)
		self.weights2 = np.random.rand(qty_outputs, qty_hlayer_nodes)

	def feed_forward(self, inputs):
		# process inputs through the network
		self.layer1 = sigmoid(np.dot(self.weights1, inputs))
		self.output = sigmoid(np.dot(self.weights2, self.layer1))
		# return highest output (networks chosen action)
		return np.argmax(self.output)
		

if __name__=='__main__':
	test_network = NeuralNetwork(6, 7, 3)
	inputs = np.array([[1, 1, 1, 1, 0, 0]]).T
	action = test_network.feed_forward(inputs)
	print('Inputs: ')
	print(inputs)
	print('\nWeights1: ')
	print(test_network.weights1)
	print('\nLayer1: ')
	print(test_network.layer1)
	print('\nWeights2: ')
	print(test_network.weights2)
	print('\nOutputs: ')
	print(test_network.output)
	print('\nChosen action:')
	print(action)