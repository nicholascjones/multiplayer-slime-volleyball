## Multiplayer Slime Volleyball
## Nicholas Jones & Brian Mann
## Twisted/PyGame Project - CSE 30332
## Prof. Collin McMillan

import sys
import math
import os
import pygame
from pygame.locals import *

class GameSpace:
	def main(self):
		# initialization
		pygame.init()
		pygame.key.set_repeat(500, 30)

		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.count = 0

		self.screen = pygame.display.set_mode(self.size)

		# set up game objects
		self.clock = pygame.time.Clock()

		# game loop
		while 1:
			# clock tick regulation
			self.clock.tick(60)

			# user input handling
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == pygame.K_q:
						sys.exit()
				elif event.type == MOUSEBUTTONUP and self.count == 0:
					self.black = 100, 100, 100
					self.count += 1
				elif event.type == MOUSEBUTTONUP and self.count == 1:
					self.black = 0, 0, 0
					self.count -= 1

			# tick game objects

			# display the game objects
			self.screen.fill(self.black)

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
