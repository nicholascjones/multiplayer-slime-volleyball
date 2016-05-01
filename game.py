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

			self.points = 0 #player number of points

			self.SpriteScale = 100 #scale for sprites to multiply by
			
			self.ground = self.gs.height
			
			## initialization differs by player
			if self.pn == 1:
				self.image = pygame.image.load("redslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()	
				self.rect.bottomleft = (0,self.ground) #player 1 values
			elif self.pn == 2:
				self.image = pygame.image.load("greenslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()
				self.rect.bottomleft = (445,self.ground) #player 2 values
			else: #if more than two players
				print "error: only two players allowed to play!"
				sys.exit(1)


			self.mv = 7 # """ TEST VALUE #velocity used""" 
			self.vx = 0 #initial x velocity
			self.vy = 0 #initial y velocity

		def tick(self):

			#movement series
			if self.rect.bottom <= self.ground:
				self.vy += self.gs.g
				self.rect = self.rect.move(0,self.vy)
				print "not ground tick"
			print "ground tick"
			self.rect = self.rect.move(self.vx,0)
			self.vx = 0


			self.by = self.rect.bottom
			self.bx = self.rect.centerx


			print "BOTTOM CENTER COORDINATES:"
			print "bottom = " + str(self.by)
			print "center = " + str(self.bx)

		def move(self,code):

			print "MOVING!!"

			print self.rect.topleft

			if code == K_RIGHT:
				#self.rect = self.rect.move(self.mv,0)
				self.vx += self.mv
			elif code == K_LEFT:
				#self.rect = self.rect.move(-self.mv,0)
				self.vx -= self.mv
			else:
				print "invalid movement"

		def jump(self):

			if self.rect.bottom >= self.ground:
				print "jump on it!"
				self.vy -= 7
				self.rect = self.rect.move(0,self.vy)
			else:
				print "no double jumping!"



class Ball(pygame.sprite.Sprite):
		def __init__(self,gs=None,x=50):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.BallScale = 15
			self.image = pygame.image.load("ball.png")
			self.image = pygame.transform.scale(self.image,(self.BallScale,self.BallScale))
			self.rect = self.image.get_rect()
			self.x = x 
			#self.y = self.gs.height/2
			self.y = 0
			self.vx = 0
			self.vy = 0
			self.rect.center = (self.x,self.y)

		def bounce(self,player):

			#bounce from player 1
			if player == 1:
				xDiff = self.gs.p1.bx-self.rect.centerx
				yDiff = self.gs.p1.by-self.rect.centery
				ang = math.atan2(yDiff,xDiff)

				""" not exactly sure what to do here """
				self.vx = math.cos(ang) * -10   #self.gs.p1.vx

				self.vy *= -1
				self.vy -= math.cos(ang)*self.gs.p1.vy
				self.rect = self.rect.move(self.vx,self.vy)

			#bounce from player 2
			elif player == 2:

				xDiff = self.gs.p2.bx-self.rect.centerx
				yDiff = self.gs.p2.by-self.rect.centery
				ang = math.atan2(yDiff,xDiff)

				""" not exactly sure what to do here """
				self.vx = math.cos(ang) * -10   #self.gs.p1.vx

				self.vy *= -1
				self.vy -= math.cos(ang)*self.gs.p2.vy
				self.rect = self.rect.move(self.vx,self.vy)

				print "PLAYER 2 BOUNCE"


			#bounce from net
			elif player == 3: #

				self.vx *= -(1.25)
				self.rect = self.rect.move(self.vx,self.vy)

				print "NET BOUNCE"

			#bounce off ceiling:
			elif player == 4:
				self.vy *= -1
				self.rect = self.rect.move(self.vx,self.vy)

			elif player == 5:
				self.vx *= -1
				self.rect = self.rect.move(self.vx,self.vy)

		def tick(self):

			# collision detection series

			print "VY = " + str(self.vy)

			#if collides with a player
			if pygame.sprite.collide_rect(self,self.gs.p1):
				print "bouncing p1!"
				self.bounce(1)
			elif pygame.sprite.collide_rect(self,self.gs.p2):
				print "bouncing p2!"
				self.bounce(2)
			elif pygame.sprite.collide_rect(self,self.gs.net):
				print "bouncing off net!"
				self.bounce(3)
			elif (self.rect.top <= 0 and self.vy < -2):
				print "bounced off ceiling"
				self.bounce(4)
			elif ( (self.rect.left <= 0 or self.rect.right >= self.gs.width) ):
				self.bounce(5)

			#if hits ground
			if self.rect.bottom < self.gs.height-10:
				self.vy += self.gs.g
				self.rect = self.rect.move(self.vx,self.vy)

			else:
				print "POINT"
				self.gs.ball = Ball(gs)



class Net(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.NetScale = 100
			self.x = 300
			self.y = self.gs.height-100
			self.image = pygame.image.load("net.png")
			self.image = pygame.transform.scale(self.image,(self.NetScale/10,self.NetScale))
			self.rect = self.image.get_rect()
			self.rect.topleft = (self.x,self.y)




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

		#Physics Objects
		
		"""NEED TO UPDATE GRAVITY"""
		self.g = 0.5

		self.screen = pygame.display.set_mode(self.size)

		# set up game objects

		self.p1 = Slime(self,self.numPlayers) #player 1
		self.numPlayers += 1
		self.p2 = Slime(self,self.numPlayers)
		self.numPlayers += 1

		self.ball = Ball(self)

		self.net = Net(self)

		self.clock = pygame.time.Clock()




		# 3) game loop
		while True:
			# 4) clock tick regulation
			self.clock.tick(60)

			# 5) user input handling
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
						self.p1.move(event.key)
					elif event.key == pygame.K_UP:
						self.p1.jump()
				elif event.type == MOUSEBUTTONUP and self.count == 0:
					self.black = 100, 100, 100
					self.count += 1
				elif event.type == MOUSEBUTTONUP and self.count == 1:
					self.black = 0, 0, 0
					self.count -= 1

			# 6) tick game objects

			self.p1.tick()

			self.p2.tick()

			self.ball.tick()

			# 7) display the game objects
			self.screen.fill(self.black)

			self.screen.blit(self.p1.image, self.p1.rect)

			self.screen.blit(self.p2.image, self.p2.rect)

			self.screen.blit(self.ball.image, self.ball.rect)

			self.screen.blit(self.net.image, self.net.rect)

		#	pygame.draw.rect

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
