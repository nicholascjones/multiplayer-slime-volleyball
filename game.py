## Multiplayer Slime Volleyball
## Nicholas Jones & Brian Mann
## Twisted/PyGame Project - CSE 30332
## Prof. Collin McMillan

import sys
import math
import os
import pygame
import random
from pygame.locals import *
	
class Slime(pygame.sprite.Sprite):
		def __init__(self, gs=None,pn=1,human=True):
			pygame.sprite.Sprite.__init__(self)

			# Member Variable Initialization
			self.gs = gs
			self.pn = pn #player number

			self.human = True

			self.points = 0 #player number of points

			self.SpriteScale = 100 #scale for sprites to multiply by
			
			self.ground = self.gs.height
			
			## initialization differs by player
			if self.pn == 1:
				self.image = pygame.image.load("redslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()	
				self.rect.centerx = self.gs.width/4 #player 1 values
				self.rect.bottom = self.ground
			elif self.pn == 2:
				self.image = pygame.image.load("greenslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()
				self.rect.centerx = 3*self.gs.width/4 #player 2 values
				self.rect.bottom = self.ground
			else: #if more than two players
				print "error: only two players allowed to play!"
				sys.exit(1)


			self.mv =  15 # """ TEST VALUE #velocity used""" 
			self.vx = 0 #initial x velocity
			self.vy = 0 #initial y velocity

		def tick(self):

			#movement series
			"""
			if self.rect.bottom < self.ground:
				print "uhhh"
				self.rect.bottom = self.ground
			"""

			if self.rect.bottom <= self.ground:
				if pygame.sprite.collide_rect(self,self.gs.net):
					if self.pn == 1:
						self.vx = -1
					elif self.pn == 2:
						self.vx = 1
				self.vy += self.gs.g
				self.rect = self.rect.move(self.vx,self.vy)
				print "not ground tick"
				print "ground tick"
			
			elif pygame.sprite.collide_rect(self,self.gs.net):
				if self.pn == 1:
					self.vx = -2
				elif self.pn == 2:
					self.vx = 2
			elif self.rect.left <= 0:
					self.vx = 2
			elif self.rect.right >= self.gs.width:
					self.vx = -2
			elif self.vx >= 1:
				self.vx -= 1
			elif self.vx <= -1:
				self.vx += 1
			else:
				pass

			self.rect = self.rect.move(self.vx,0)


			self.by = self.rect.bottom
			self.bx = self.rect.centerx


			print "BOTTOM CENTER COORDINATES:"
			print "bottom = " + str(self.by)
			print "center = " + str(self.bx)

		def move(self,code):


			if self.human == True:
				print "MOVING!!"

				print self.rect.topleft

				if code == K_RIGHT:
				#	self.rect = self.rect.move(self.mv,0)
					self.vx += self.mv/2
				elif code == K_LEFT:
				#	self.rect = self.rect.move(-self.mv,0)
					self.vx -= self.mv/2
				else:
					print "invalid movement"

			else:
				self.vx = self.gs.ball.vx

		def jump(self):

			if self.rect.bottom >= self.ground:
				print "jump on it!"
				self.vy -= 7
				self.rect = self.rect.move(0,self.vy)
			else:
				print "no double jumping!"



class Ball(pygame.sprite.Sprite):
		def __init__(self,gs=None,winner=1):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.BallScale = 15
			self.image = pygame.image.load("ball.png")
			self.image = pygame.transform.scale(self.image,(self.BallScale,self.BallScale))
			self.rect = self.image.get_rect()

			#determines who "serves" based on winner
			if winner == 1:
				self.x = random.randint(self.gs.width/8,(3*self.gs.width/8))
			else: #if player 2 wins point
				self.x = random.randint((5*self.gs.width/8),(7*self.gs.width/8))
			#self.y = self.gs.height/2
			self.y = 0
			self.vx = 0
			self.vy = 0
			self.rect.center = (self.x,self.y)

		def bounce(self,player):


			rf = random.randint(-1,1)
			rs = random.random()
			#bounce from player 1
			if player == 1:
				xDiff = self.gs.p1.bx-self.rect.centerx
				yDiff = self.gs.p1.by-self.rect.centery#+(xDiff/self.rect.centery)
				ang = math.atan2(yDiff,xDiff)

				""" not exactly sure what to do here """
				self.vx = math.cos(ang) * -12.5  #self.gs.p1.vx
				self.vx += math.cos(ang)*self.gs.p1.vx
				self.vx += (int(rf*rs))

				if abs(self.vx) < 1:
					self.vx+=random.uniform(-1.5,1.5)

				self.vy *= -0.9
				self.vy -= math.cos(ang)*self.gs.p1.vy
				self.rect = self.rect.move(self.vx,self.vy)

			#bounce from player 2
			elif player == 2:

				xDiff = self.gs.p2.bx-self.rect.centerx
				yDiff = self.gs.p2.by-self.rect.centery#+(xDiff/self.rect.centery)
				ang = math.atan2(yDiff,xDiff)

				""" not exactly sure what to do here """
				self.vx = math.cos(ang) * -12.5 #self.gs.p1.vx
				self.vx += math.cos(ang)*self.gs.p2.vx
				self.vx += (int(rf*rs))

				if abs(self.vx) < 1:
					self.vx+=random.uniform(-1.5,1.5)

				self.vy *= -0.9
				self.vy -= math.cos(ang)*self.gs.p2.vy
				self.rect = self.rect.move(self.vx,self.vy)

				print "PLAYER 2 BOUNCE"


			#bounce from net
			elif player == 3: #

				if (self.rect.centery >= 375 and self.rect.centery <= 385):
					self.vy *= int(-0.75)
					print "TOP NET BOUNCE OMG"
				else:

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
			print "VX = " + str(self.vx)

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
			elif (self.rect.top <= 0 and self.vy < -2 and self.gs.ceiling == True):
				print "bounced off ceiling"
				self.bounce(4)
			elif ( (self.rect.left <= 0 or self.rect.right >= self.gs.width) and self.gs.walls == True):
				print "bounced off wall"
				self.bounce(5)

			#if hits ground
			if self.rect.bottom < self.gs.height-10:
				self.vy += self.gs.ballG
				self.rect = self.rect.move(self.vx,self.vy)

			else:
				print "point awarded"

				if self.rect.centerx <= self.gs.width/2:
					self.gs.p2.points += 1
					self.gs.ball = Ball(gs,2)
				else:
					self.gs.p1.points += 1
					self.gs.ball = Ball(gs,1)

				print "PLAYER 1 POINTS = " + str(self.gs.p1.points)
				print "PLAYER 2 POINTS = " + str(self.gs.p2.points)



class Net(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.NetScale = 100
			#self.x = 300
			self.y = self.gs.height-100
			self.image = pygame.image.load("net.png")
			self.image = pygame.transform.scale(self.image,(self.NetScale/10,self.NetScale))
			self.rect = self.image.get_rect()
			self.rect.centerx = self.gs.width/2
			self.rect.bottom = self.gs.height

			print "net topleft = " + str(self.rect.topleft)


class Win(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs

		def tick(self):
			if self.gs.p1.points == self.gs.maxPts:
				self.win(1)
			elif self.gs.p2.points == self.gs.maxPts:
				self.win(2)
			else:
				pass

		def win(self,player):
				print "Player " + str(player) + " Wins!"
				self.gs.gameOver = True




class GameSpace:
	def main(self):
		# initialization
		pygame.init()
		pygame.key.set_repeat(500, 30)

		# General Game Variables
		self.size = self.width, self.height = 640, 480
		self.black = 100, 100, 100 #gray background preferable
		self.count = 0

		self.title = "Slime Volleyball"

		#game over flag
		self.gameOver = False

		self.numPlayers = 1 #default number of players

		self.maxPts = 21

		#Physics Objects
		
		"""NEED TO UPDATE GRAVITY"""
		self.g = 0.5
		self.ballG = 0.35

		#flags to enable ceilings and walls
		self.ceiling = True
		self.walls = True

		self.screen = pygame.display.set_mode(self.size)

		# set up game objects

		self.p1 = Slime(self,self.numPlayers) #player 1
		self.numPlayers += 1
		self.p2 = Slime(self,self.numPlayers,True) #computer
		self.numPlayers += 1

		self.ball = Ball(self)

		self.win = Win(self)

		self.net = Net(self)

		self.clock = pygame.time.Clock()




		# 3) game loop
		while self.gameOver == False:
			# 4) clock tick regulation
			self.clock.tick(60)

			# 5) user input handling
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
						self.p1.move(event.key)

					if event.key == pygame.K_UP:
						self.p1.jump()

			# 6) tick game objects

			self.p1.tick()

			self.p2.tick()

			self.ball.tick()

			self.win.tick()

			# 7) display the game objects
			self.screen.fill(self.black)

			self.screen.blit(self.p1.image, self.p1.rect)

			self.screen.blit(self.p2.image, self.p2.rect)

			self.screen.blit(self.ball.image, self.ball.rect)

			self.screen.blit(self.net.image, self.net.rect)

			#displaying red slime score
			self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.p1.points), True, (252,13,27)), ((self.width/4),20))

			#displaying green slime score
			self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.p2.points), True, (42,253,52)), ((3*self.width/4),20))

			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.title), True, (255,255,255)), ((5*self.width/16)+15,20))


			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
