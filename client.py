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

			self.SpriteScale = 100 #scale for sprites to multiply by
			self.ground = self.gs.height
			
			## initialization differs by player
			if self.pn == 1:
				self.image = pygame.image.load("redslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()
				self.rect.bottomleft = (0, self.ground) #player 1 values
			elif self.pn == 2:
				self.image = pygame.image.load("greenslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()
				self.rect.bottomleft = (445, self.ground) #player 2 values
			else: #if more than two players
				print "error: only two players allowed to play!"
				sys.exit(1)


			self.mv = 7 # """ TEST VALUE #velocity used""" 
			self.vx = 0 #initial x velocity
			self.vy = 0 #initial y velocity

		def tick(self):
			if self.rect.bottom <= self.ground:
				self.vy += self.gs.g
				self.rect = self.rect.move(0, self.vy)
			self.rect = self.rect.move(self.vx, 0)
			self.vx = 0

		def move(self,code):

			#print "MOVING!!"

			#print self.rect.topleft

			if code == K_d:
				#self.rect = self.rect.move(self.mv,0)
				self.vx += self.mv
			elif code == K_a:
				#self.rect = self.rect.move(-self.mv,0)
				self.vx -= self.mv
			#else:
				#print "invalid movement"

		def jump(self):
			if self.rect.bottom >= self.ground:
				self.vy -= 7
				self.rect = self.rect.move(0, self.vy)

class Ball(pygame.sprite.Sprite):
		def __init__(self,gs=None,x=0):
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
			self.rect.topleft = (self.x,self.y)

		def bounce(self):
			self.vy *= -1
			self.rect = self.rect.move(0, self.vy)

		def tick(self):
			if (pygame.sprite.collide_rect(self, self.gs.p) or pygame.sprite.collide_rect(self, self.gs.e)):
				self.bounce()
			elif self.rect.bottom < self.gs.height-10:
				self.vy += self.gs.g
				self.rect = self.rect.move(0, self.vy)

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
		self.e = None
		self.ball = None

		"""NEED TO UPDATE GRAVITY"""
		self.g = 0.5

	def new_line(self, line):
		self.line = line
		if self.line == str(1) or self.line == str(2) or self.line == "Server is full!":
			self.connectionMade()
		else:
			if self.e != None:
				self.e.rect.centerx = int(self.line)
	def connectionMade(self):
		if self.line == str(1) or self.line == str(2):
			self.net = Net(self)
			self.ball = Ball(self)
			self.value = int(self.line)
			self.p = Slime(self, self.value)
			if self.value == 1:
				self.e = Slime(self, self.value+1)
			if self.value == 2:
				self.e = Slime(self, self.value-1)
		elif self.line == "Server is full!":
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
					self.p.move(event.key)
				elif event.key == pygame.K_SPACE:
					self.p.jump()	

		if self.p != None:
			self.p.tick()
		if self.e != None:
			self.e.tick()
		if self.ball != None:
			self.ball.tick()

		self.screen.fill(self.black)
		if self.p != None:
			self.screen.blit(self.p.image, self.p.rect)
			self.screen.blit(self.e.image, self.e.rect)
			self.screen.blit(self.ball.image, self.ball.rect)
			self.screen.blit(self.net.image, self.net.rect)

		pygame.display.flip()

c = Client()

lc = LoopingCall(c.tick)
lc.start(1.0/60)
reactor.connectTCP(SERVER_HOST, SERVER_PORT, ClientFactory(c.new_line))
reactor.run()
lc.stop()
