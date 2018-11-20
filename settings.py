"""
settings for neural network visualiser
"""

TITLE = 'Neural Network Visualiser'
TILESIZE = 16
MAP_WIDTH = 32
MAP_HEIGHT = 32
WIDTH = TILESIZE * MAP_WIDTH
HEIGHT = TILESIZE * MAP_HEIGHT
FPS = 1000000

POPULATION_SIZE = 100
ELITISM = 0.5

# neural network settings
INPUTS = 6
HIDDEN_NODES = 7
OUTPUTS = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (200, 0, 0)