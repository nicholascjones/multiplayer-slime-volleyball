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
from pygame.locals import *

SERVER_HOST = "localhost"
SERVER_PORT = 40025

class Slime(pygame.sprite.Sprite):
		def __init__(self, gs=None,pn=1):
			pygame.sprite.Sprite.__init__(self)

			# Member Variable Initialization
			self.gs = gs
			self.pn = pn #player number

			self.SpriteScale = 150 #scale for sprites to multiply by
			
			
			## initialization differs by player
			if self.pn == 1:
				self.image = pygame.image.load("redslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,self.SpriteScale))
				self.rect = self.image.get_rect()
				self.rect.topleft = (0,375) #player 1 values
			elif self.pn == 2:
				self.image = pygame.image.load("greenslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,self.SpriteScale))
				self.rect = self.image.get_rect()
				self.rect.topleft = (445,375) #player 2 values
			else: #if more than two players
				print "error: only two players allowed to play!"
				sys.exit(1)


			self.mv = 5 # """ TEST VALUE #velocity used""" 
			self.vx = 0 #initial x velocity
			self.vy = 0 #initial y velocity

		def tick(self):

			print "tick"

		def move(self,code):

			#print "MOVING!!"

			#print self.rect.topleft

			if code == K_d:
				self.rect = self.rect.move(self.mv,0)
			elif code == K_a:
				self.rect = self.rect.move(-self.mv,0)
			else:
				print "invalid movement"

class Net(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.NetScale = 100
			self.x = self.gs.width/2 - 50
			self.y = self.gs.height-100
			self.image = pygame.image.load("net.png")
			self.image = pygame.transform.scale(self.image,(self.NetScale,self.NetScale))
			self.rect = self.image.get_rect()
			self.rect.topleft = (self.x,self.y)

class Ball(pygame.sprite.Sprite):
		def __init__(self,gs=None,x=0):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.BallScale = 20
			self.image = pygame.image.load("ball.png")
			self.image = pygame.transform.scale(self.image,(self.BallScale,self.BallScale))
			self.rect = self.image.get_rect()
			self.x = x 
			#self.y = self.gs.height/2
			self.y = 0
			self.rect.topleft = (self.x,self.y)

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
		#pygame.init()
		#pygame.key.set_repeat(500, 30)

		# General Game Variables
		self.size = self.width, self.height = 640, 480
		#self.screen = pygame.display.set_mode(self.size)
		#self.black = 0, 0, 0

		#Physics Objects
		"""NEED TO UPDATE GRAVITY"""
		self.g = None  

		# set up game objects
		self.p1 = None
		self.p2 = None
		self.ball = Ball(self)
		self.net = Net(self)

	def addplayer(self, player):
		if player == 1:
			self.p1 = Slime(self, 1)
		else:
			self.p2 = Slime(self, 2)

	def tick(self):
		#for event in pygame.event.get():
		#	if event.type == QUIT:
		#		reactor.stop()

		#self.screen.fill(self.black)
		if self.p1 != None:
			#self.screen.blit(self.p1.image, self.p1.rect)
			if self.p2 != None:
				tracker.player1.transport.write(str(self.p2.rect.centerx))
		if self.p2 != None:
			#self.screen.blit(self.p2.image, self.p2.rect)
			tracker.player2.transport.write(str(self.p1.rect.centerx))
		#self.screen.blit(self.ball.image, self.ball.rect)
		#self.screen.blit(self.net.image, self.net.rect)

tracker = Tracker()
gs = GameSpace()

lc = LoopingCall(gs.tick)
lc.start(1.0/60)
reactor.listenTCP(SERVER_PORT, ServerFactory())
reactor.run()
lc.stop()
