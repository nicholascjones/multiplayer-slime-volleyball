## Multiplayer Slime Volleyball
## Nicholas Jones & Brian Mann
## Twisted/PyGame Project - CSE 30332
## Prof. Collin McMillan

from twisted.internet.protocol import ClientFactory
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

class ClientProtocol(Protocol):

	def __init__(self, recv):
		self.recv = recv
		c.protocol = self

	def dataReceived(self, data):
		self.recv(data)

	def connectionMade(self):
		print "Connected to server!"

	def connectionLost(self, reason):
		c.exit = True

class ClientFactory(ClientFactory):

	def __init__(self, recv):
		self.protocol = ClientProtocol
		self.recv = recv

	def buildProtocol(self, addr):
		return ClientProtocol(self.recv)

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
			#else:
				#print "invalid movement"

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

class Client(object):

	def __init__(self):
		#1) initialization
		self.exit = False
		pygame.init()
		pygame.key.set_repeat(500, 30)
		# game variables
		self.size = self.width, self.height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		self.black = 0, 0, 0
		self.p = None

		"""NEED TO UPDATE GRAVITY"""
		self.g = None

	def new_line(self, line):
		self.line = line
		self.connectionMade()

	def connectionMade(self):
		if self.line == str(1) or self.line == str(2):
			self.ball = Ball(self)
			self.net = Net(self)
			self.p = Slime(self, int(self.line))
		elif self.line == "Disconnect":
			print self.line
			reactor.stop()
		else:
			print self.line
			reactor.stop()

	def tick(self):
		if c.exit == True:
			reactor.stop()
		for event in pygame.event.get():
			if event.type == QUIT:
				reactor.stop()
			elif event.type == KEYDOWN:
				if event.key == pygame.K_q:
					reactor.stop()
				elif (event.key == pygame.K_a or event.key == pygame.K_d):
					self.protocol.transport.write(str(event.key))

		self.screen.fill(self.black)
		if self.p != None:
			self.screen.blit(self.p.image, self.p.rect)
			self.screen.blit(self.ball.image, self.ball.rect)
			self.screen.blit(self.net.image, self.net.rect)

		pygame.display.flip()

c = Client()

lc = LoopingCall(c.tick)
lc.start(1.0/60)
reactor.connectTCP(SERVER_HOST, SERVER_PORT, ClientFactory(c.new_line))
reactor.run()
lc.stop()
