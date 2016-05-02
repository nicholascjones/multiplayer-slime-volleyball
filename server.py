## Multiplayer Slime Volleyball
## Nicholas Jones & Brian Mann
## Twisted/PyGame Project - CSE 30332
## Prof. Collin McMillan

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import sys
import math
import os
import pygame
import random
from pygame.locals import *

SERVER_HOST = "localhost"
SERVER_PORT = 40025

class Slime(pygame.sprite.Sprite):
		def __init__(self, gs=None,pn=1,human=True):
			pygame.sprite.Sprite.__init__(self)

			# Member Variable Initialization
			self.gs = gs
			self.pn = pn #player number

			self.human = human

			self.points = 0 #player number of points

			self.SpriteScale = 100 #scale for sprites to multiply by
			
			self.ground = self.gs.height
			
			## initialization differs by player
			if self.pn == 1:
				self.image = pygame.image.load("redslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()

				self.rect.centerx = self.gs.width/4
				# player 1 values
				self.rect.bottom = self.ground
			elif self.pn == 2:
				self.image = pygame.image.load("greenslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()
				self.rect.centerx = 3*self.gs.width/4
				#player 2 values
				self.rect.bottom = self.ground 

			self.mv = 15 # """ TEST VALUE #velocity used""" 
			self.vx = 0 #initial x velocity
			self.vy = 0 #initial y velocity

		def tick(self):

			#movement series
			if self.rect.bottom <= self.ground:
				if pygame.sprite.collide_rect(self,self.gs.net):
					if self.pn == 1:
						self.vx = -1
					elif self.pn == 2:
						self.vx = 1
				self.vy += self.gs.g
				self.rect = self.rect.move(self.vx,self.vy)
			
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

		def move(self,code):

			if self.human == True:

				if code == K_d:
				#	self.rect = self.rect.move(self.mv,0)
					self.vx += self.mv/2
				elif code == K_a:
				#	self.rect = self.rect.move(-self.mv,0)
					self.vx -= self.mv/2

			else:
				self.vx = self.gs.ball.vx

		def jump(self):

			if self.rect.bottom >= self.ground:
				self.vy -= 7
				self.rect = self.rect.move(0,self.vy)

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

				self.vy *= -0.9
				self.vy -= math.cos(ang)*self.gs.p2.vy
				self.rect = self.rect.move(self.vx,self.vy)

			#bounce from net
			elif player == 3: #

				if (self.rect.centery >= 375 and self.rect.centery <= 385):
					self.vy *= int(-0.75)
				else:
					self.vx *= -(1.25)
					self.rect = self.rect.move(self.vx,self.vy)

			#bounce off ceiling:
			elif player == 4:
				self.vy *= -1
				self.rect = self.rect.move(self.vx,self.vy)

			elif player == 5:
				self.vx *= -1
				self.rect = self.rect.move(self.vx,self.vy)

		def tick(self):

			# collision detection series
			#if collides with a player
			if pygame.sprite.collide_rect(self,self.gs.p1):
				self.bounce(1)
			elif pygame.sprite.collide_rect(self,self.gs.p2):
				self.bounce(2)
			elif pygame.sprite.collide_rect(self,self.gs.net):
				self.bounce(3)
			elif (self.rect.top <= 0 and self.vy < -2 and self.gs.ceiling == True):
				self.bounce(4)
			elif ( (self.rect.left <= 0 or self.rect.right >= self.gs.width) and self.gs.walls == True):
				self.bounce(5)

			#if hits ground
			if self.rect.bottom < self.gs.height-10:
				self.vy += self.gs.g
				self.rect = self.rect.move(self.vx,self.vy)

			else:

				if self.rect.centerx <= self.gs.width/2:
					self.gs.p2.points += 1
					self.gs.ball = Ball(gs,2)
				else:
					self.gs.p1.points += 1
					self.gs.ball = Ball(gs,1)


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

class Server(Protocol):

	def __init__(self, players, addr):
		self.players = players
		self.addr = addr
		self.gs = gs
		if len(self.players) == 0:
			tracker.player1 = self
		elif len(self.players) == 1:
			tracker.player2 = self

	def connectionMade(self):
		if len(self.players) == 0:
			new = 'player_' + str(len(self.players) + 1)
			self.players.append(new)
			self.gs.addplayer(len(self.players))
			print "Player 1 connected!"
			self.transport.write(str(1))
		elif len(self.players) == 1:
			new = 'player_' + str(len(self.players) + 1)
			self.players.append(new)
			self.gs.addplayer(len(self.players))
			print "Player 2 connected!"
			self.transport.write(str(2))
		else:
			self.transport.write("Server is full!")
	def connectionLost(self, reason):
		if self == tracker.player1:
			print "Player 1 disconnected!"
			if self.gs.p2 != None:
				tracker.player2.transport.loseConnection()
		elif self == tracker.player2:
			print "Player 2 disconnected!"
			tracker.player1.transport.loseConnection()
		else:
			return
		self.gs.p1 = None
		self.gs.p2 = None
		self.players.pop()

	def dataReceived(self, data):
		if data == str(100):
			key = pygame.K_d
		elif data == str(97):
			key = pygame.K_a
		elif data == str(32):
			if self == tracker.player1:
				self.gs.p1.jump()
				return
			if self == tracker.player2:
				self.gs.p2.jump()
				return
		if self == tracker.player1:
			self.gs.p1.move(key)
		elif self == tracker.player2:
			self.gs.p2.move(key)

class ServerFactory(Factory):

	def __init__(self):
		self.players = []

	def buildProtocol(self, addr):
		return Server(self.players, addr)

class Tracker:
	
	def __init__(self):
		self.player1 = Server
		self.player2 = Server

class GameSpace:

	def __init__(self):
		# initialization

		# General Game Variables
		self.size = self.width, self.height = 640, 480

		#Physics Objects
		"""NEED TO UPDATE GRAVITY"""
		self.g = 0.5

		# set up game objects
		self.p1 = None
		self.p2 = None
		self.ball = Ball(self)
		self.net = Net(self)
		self.ceiling = True
		self.walls = True

	def addplayer(self, player):
		if player == 1:
			self.p1 = Slime(self, 1)
		else:
			self.p2 = Slime(self, 2)

	def tick(self):
		if self.p1 != None:
			self.p1.tick()
			if self.p2 != None:
				tracker.player1.transport.write(str(self.p2.rect.centerx)+"|"+str(self.p2.rect.centery)+"|"+str(self.ball.rect.centerx)+"|"+str(self.ball.rect.centery))
		if self.p2 != None:
			self.p2.tick()
			self.ball.tick()
			tracker.player2.transport.write(str(self.p1.rect.centerx)+"|"+str(self.p1.rect.centery)+"|"+str(self.ball.rect.centerx)+"|"+str(self.ball.rect.centery))


tracker = Tracker()
gs = GameSpace()

lc = LoopingCall(gs.tick)
lc.start(1.0/60)
reactor.listenTCP(SERVER_PORT, ServerFactory())
reactor.run()
lc.stop()
