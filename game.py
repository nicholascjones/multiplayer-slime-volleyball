## Multiplayer Slime Volleyball
## Nicholas Jones & Brian Mann
## Twisted/PyGame Project - CSE 30332
## Prof. Collin McMillan

import sys
import math
import os
import pygame
from pygame.locals import *
	
class Slime(pygame.sprite.Sprite):
	def __init__(self, gs=None, x=0, y=375):
		pygame.sprite.Sprite.__init__(self)

		# Member Variable Initialization
		self.gs = gs
		self.image = pygame.image.load("redslime.png") #sprite image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
		self.mv = 5 # TEST VALUE #velocity used""" 
		self.vx = 0 #initial x velocity
		self.vy = 0 #initial y velocity

	def tick(self):

		print "tick"

	def move(self,code):

		print "MOVING!!"

		print self.rect.topleft

		if code == K_RIGHT:
			self.rect = self.rect.move(self.mv,0)
		elif code == K_LEFT:
			self.rect = self.rect.move(-self.mv,0)
		elif code == K_DOWN:
			self.rect = self.rect.move(0,self.mv)
		else:
			print "invalid"

		





class GameSpace:
	def main(self):
		# initialization
		pygame.init()
		pygame.key.set_repeat(500, 30)

		# General Game Variables
		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.count = 0

		

		self.screen = pygame.display.set_mode(self.size)

		# set up game objects

		self.p1 = Slime(self) #player 1

		self.clock = pygame.time.Clock()


		#Physics Objects
		"""NEED TO UPDATE GRAVITY"""
		self.g = None  

		# 3) game loop
		while True:
			# 4) clock tick regulation
			self.clock.tick(60)

			# 5) user input handling
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == pygame.K_q:
						sys.exit()
					elif (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN):
						self.p1.move(event.key)
				elif event.type == MOUSEBUTTONUP and self.count == 0:
					self.black = 100, 100, 100
					self.count += 1
				elif event.type == MOUSEBUTTONUP and self.count == 1:
					self.black = 0, 0, 0
					self.count -= 1

			# 6) tick game objects

			# 7) display the game objects
			self.screen.fill(self.black)

			self.screen.blit(self.p1.image, self.p1.rect)

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
