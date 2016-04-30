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
	def __init__(self, gs=None,pn=1):
		pygame.sprite.Sprite.__init__(self)

		# Member Variable Initialization
		self.gs = gs
		self.pn = pn #player number
		self.image = pygame.image.load("redslime.png") #sprite image
		self.rect = self.image.get_rect()
		if self.pn == 1:
			self.rect.topleft = (0,375) #player 1 values
		elif self.pn == 2:
			self.rect.topleft = (445,375) #player 2 values
		else: #if more than two players
			print "error: only two players allowed to play!"
			sys.exit(1)

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


class Ball(pygame.sprite.Sprite):
		def __init__(self,x=0):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.image = pygame.image.load("ball.png")
			self.rect = self.image.get_rect()
			self.x = x
			#self.y = self.gs.height/2
			self.y = 0
		#	self.rect.center = (self.x,self.y)





class GameSpace:
	def main(self):
		# initialization
		pygame.init()
		pygame.key.set_repeat(500, 30)

		# General Game Variables
		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.count = 0

		self.numPlayers = 1 #default number of players

		

		self.screen = pygame.display.set_mode(self.size)

		# set up game objects

		self.p1 = Slime(self,self.numPlayers) #player 1
		self.numPlayers += 1
		self.p2 = Slime(self,self.numPlayers)
		self.numPlayers += 1

		self.ball = Ball(self)

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

			self.screen.blit(self.p2.image, self.p2.rect)

			self.screen.blit(self.ball.image, self.ball.rect)

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
