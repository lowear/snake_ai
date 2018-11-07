"""
Neural Network Visulaiser
Teaches an AI to play Snake
"""

import sys
import pygame as pg
from game import Game

if __name__ == '__main__':
	g = Game()
	g.show_start_screen()
	g.new_simulation()
	pg.quit()
	sys.exit()