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
import random
from pygame.locals import *

SERVER_HOST = "localhost"
SERVER_PORT = 40025

class ClientProtocol(Protocol):
	# basic Twisted client
	def __init__(self, recv):
		# link the client to the gamespace
		self.recv = recv
		c.protocol = self

	def dataReceived(self, data):
		# send all data from the client to the gamespace
		self.recv(data)

	def connectionMade(self):
		print "Connected to server!"

	def connectionLost(self, reason):
		c.exit = True

class ClientFactory(ClientFactory):
	# basic Twisted clientfactory
	def __init__(self, recv):
		self.protocol = ClientProtocol
		self.recv = recv

	def buildProtocol(self, addr):
		return ClientProtocol(self.recv)

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
				xDiff = self.gs.p.bx-self.rect.centerx
				yDiff = self.gs.p.by-self.rect.centery#+(xDiff/self.rect.centery)
				ang = math.atan2(yDiff,xDiff)

				""" not exactly sure what to do here """
				self.vx = math.cos(ang) * -12.5  #self.gs.p1.vx
				self.vx += math.cos(ang)*self.gs.p.vx
				self.vx += (int(rf*rs))

				self.vy *= -0.9
				self.vy -= math.cos(ang)*self.gs.p.vy
				self.rect = self.rect.move(self.vx,self.vy)

			#bounce from player 2
			elif player == 2:

				xDiff = self.gs.e.bx-self.rect.centerx
				yDiff = self.gs.e.by-self.rect.centery#+(xDiff/self.rect.centery)
				ang = math.atan2(yDiff,xDiff)

				""" not exactly sure what to do here """
				self.vx = math.cos(ang) * -12.5 #self.gs.p1.vx
				self.vx += math.cos(ang)*self.gs.e.vx
				self.vx += (int(rf*rs))

				self.vy *= -0.9
				self.vy -= math.cos(ang)*self.gs.e.vy
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
			if pygame.sprite.collide_rect(self,self.gs.p):
				self.bounce(1)
			elif pygame.sprite.collide_rect(self,self.gs.e):
				self.bounce(2)
			elif pygame.sprite.collide_rect(self,self.gs.net):
				self.bounce(3)
			elif (self.rect.top <= 0 and self.vy < -2 and self.gs.ceiling == True):
				self.bounce(4)
			elif ( (self.rect.left <= 0 or self.rect.right >= self.gs.width) and self.gs.walls == True):
				self.bounce(5)

			#if hits ground
			if self.rect.bottom < self.gs.height-10:
				self.vy += self.gs.ballG
				self.rect = self.rect.move(self.vx,self.vy)

			else:

				if self.rect.centerx <= self.gs.width/2:
					self.gs.e.points += 1
					self.gs.ball = Ball(self.gs,2)
				else:
					self.gs.p.points += 1
					self.gs.ball = Ball(self.gs,1)


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

class Client(object):

	def __init__(self):
		#1) initialization
		self.exit = False
		pygame.init()
		pygame.key.set_repeat(500, 30)
		# game variables
		self.size = self.width, self.height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		self.black = 100, 100, 100
		self.p = None
		self.e = None
		self.ball = None
		self.connected = False

		"""NEED TO UPDATE GRAVITY"""
		self.g = 0.5
		self.ballG = 0.35

		self.ceiling = True
		self.walls = True

	def new_line(self, line):
		# how each client updates the game from the server
		self.line = line
		# determine what is being sent over the network
		if self.connected == False and (self.line == str(1) or self.line == str(2) or self.line == "Server is full!"):
			self.connected = True
			self.connectionMade()
		else:
			# separate the string for data processing
			components = self.line.split("|")
			x = components[0]
			y = components[1]
			bx = components[2]
			by = components[3]
			if self.e != None:
				self.e.rect.centerx = int(x)
				self.e.rect.bottom = int(y)
			if self.ball != None:
				self.ball.rect.centerx = int(bx)
				self.ball.rect.centery = int(by)

	def connectionMade(self):
		# determine which player the client is
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
		# update the screen info and obtain user input
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
					self.protocol.transport.write(str(event.key))
					self.p.jump()	

		# only tick oneself
		if self.p != None:
			self.p.tick()

		self.screen.fill(self.black)
		if self.p != None:
			self.screen.blit(self.p.image, self.p.rect)
			self.screen.blit(self.e.image, self.e.rect)
			self.screen.blit(self.ball.image, self.ball.rect)
			self.screen.blit(self.net.image, self.net.rect)

		pygame.display.flip()

c = Client()

lc = LoopingCall(c.tick)
lc.start(1.0/30)
reactor.connectTCP(SERVER_HOST, SERVER_PORT, ClientFactory(c.new_line))
reactor.run()
lc.stop()
