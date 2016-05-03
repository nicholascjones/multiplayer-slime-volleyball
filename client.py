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

			self.mv =  8 # """ TEST VALUE #velocity used""" 
			self.vx = 0 #initial x velocity
			self.vy = 0 #initial y velocity

		def tick(self):

			#movement series
			if self.rect.bottom > self.ground:
				self.rect.bottom = self.ground

			

			if self.rect.bottom < self.ground:
				if pygame.sprite.collide_rect(self,self.gs.net):
					if self.pn == 1:
						self.vx = -1
					elif self.pn == 2:
						self.vx = 1
					elif self.rect.left <= 0:
						self.vx = 2
					elif self.rect.right >= self.gs.width:
						self.vx = -2
					elif self.vx >= 1:
						self.vx -= 1
					elif self.vx <= -1:
						self.vx += 1
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

			if (self.rect.bottom <= self.ground) and (self.rect.bottom > self.ground-5):
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
			if self.gs.challenge == False:
				self.y = 0
			else:
				self.y = self.gs.height/4 + 20
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
			elif self.gs.challenge == True:
				if pygame.sprite.collide_rect(self, self.gs.ceiling):
					self.bounce(4)

			#if hits ground
			if self.rect.bottom < self.gs.height-10:
				self.vy += self.gs.ballG
				self.rect = self.rect.move(self.vx,self.vy)

			else:
				if self.rect.centerx <= self.gs.width/2:
					self.point(2)
				else:
					self.point(1)
					

		def point(self,player):

			if player == 1:
				self.gs.p1.points += 1
				self.gs.ball = Ball(gs,1)

			else: #if player is 2
				self.gs.p2.points += 1
				self.gs.ball = Ball(gs,2)


class Net(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.NetScale = 100
			#self.x = 300
			self.y = self.gs.height-100
			self.image = pygame.image.load("net.png")
			if self.gs.challenge == False:
				self.image = pygame.transform.scale(self.image,(self.NetScale/10,self.NetScale))
			else:
				self.image = pygame.transform.scale(self.image,(self.NetScale/10,int(1.5*self.NetScale)))
			self.rect = self.image.get_rect()
			self.rect.centerx = self.gs.width/2
			self.rect.bottom = self.gs.height

class Win(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs

		def tick(self):
			if self.gs.p.points >= self.gs.maxPts:
				self.win(1)
			elif self.gs.e.points >= self.gs.maxPts:
				self.win(2)
			else:
				pass

		def win(self,player):
				self.gs.gameOver = True
				self.gs.endGame = EndGame(player, self.gs)

class Menu(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.image = pygame.image.load("redslime.png")
			self.image = pygame.transform.scale(self.image,(200,120))
			self.rect = self.image.get_rect()
			self.rect.center = (self.gs.width/2,(3*self.gs.height/4)+30)
			self.isMenu = True

			self.l2 = "Ceilings are ON. Press 'c' to toggle." 
			self.l3 = "Walls are ON. Press 'w' to toggle."
			self.l4 = "This game is being played to " + str(self.gs.maxPts) + " points,"
			self.l6 = "press the up or down arrows to change."
			self.l5 = "Press ENTER to start!"

		def tick(self):

			if self.gs.ceiling == True:
				self.l2 = "Ceilings are ON. Press 'c' to toggle." 
			else:
				self.l2 = "Ceilings are OFF. Press 'c' to toggle." 

			if self.gs.walls == True:
				self.l3 = "Walls are ON. Press 'w' to toggle."
			else:
				self.l3 = "Walls are OFF. Press 'w' to toggle."

			self.l4 = "This game is being played to " + str(self.gs.maxPts) + " points,"



		def changePoints(self,code):

			if code == pygame.K_UP:
				self.gs.maxPts += 1
			elif self.gs.maxPts > 1:
				self.gs.maxPts -= 1

		def toggleCeilings(self):
			if self.gs.ceiling == True:
				self.gs.ceiling = False
			else:
				self.gs.ceiling = True

		def toggleWalls(self):
			if self.gs.walls == True:
				self.gs.walls = False
			else:
				self.gs.walls = True

class EndGame(pygame.sprite.Sprite):
		def __init__(self,winner,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			if winner == 1:
				self.image = pygame.image.load("redslime.png")
				self.winMsg = "Congratulations, Player 1!"
				self.loseMsg = "Player 2...better luck next time!"
			else:
				self.image = pygame.image.load("greenslime.png")
				self.winMsg = "Congratulations, Player 2"
				self.loseMsg = "Player 1...better luck next time!"

			self.win2 = "YOU WIN!"
			self.image = pygame.transform.scale(self.image,(200,120))
			self.rect = self.image.get_rect()
			self.rect.center = (self.gs.width/2,(3*self.gs.height/4)+30)
			self.rMsg = "To play a CHALLENGE GAME, press ENTER"
			self.qMsg = "To quit, click or press the 'q' key."
			self.gameOver = True

			self.gs.p.points = 0
			self.gs.e.points = 0

class Ceiling(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.CeilScale = 1000
		self.image = pygame.image.load("ceiling.png")
		self.image = pygame.transform.scale(self.image,(self.CeilScale,10))
		self.rect = self.image.get_rect()
		self.rect.centerx = self.gs.width/2
		self.rect.centery = self.gs.height/4

class Client(object):

	def __init__(self):
		#1) initialization
		self.exit = False
		pygame.init()
		pygame.key.set_repeat(1, 50)
		# game variables
		self.size = self.width, self.height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		self.black = 100, 100, 100
		self.title = "Slime Volleyball"
		self.p = None
		self.e = None
		self.ball = None
		self.gameOver = False
		self.challenge = False
		self.connected = False
		self.maxPts = 25
		self.menu = Menu(self)
		self.win = Win(self)

		"""NEED TO UPDATE GRAVITY"""
		self.g = 0.5
		self.ballG = 0.35

		self.ceiling = True
		self.walls = True

	def new_line(self, line):
		# how each client updates the game from the server
		self.line = line
		if self.line == "win1":
			self.win.win(1)
		elif self.line == "win2":
			self.win.win(2)
		# determine what is being sent over the network
		if self.connected == False and (self.line == str(1) or self.line == str(2) or self.line == "Server is full!"):
			self.connected = True
			self.connectionMade()
			return
		if self.menu.isMenu == False:
			# separate the string for data processing
			components = self.line.split("|")
			try:
				px = components[0]
				py = components[1]
				ex = components[2]
				ey = components[3]
				bx = components[4]
				by = components[5]
				ppoints = components[6]
				epoints = components[7]
			except:
				return
			if self.p != None:
				self.p.rect.centerx = int(px)
				self.p.rect.bottom = int(py)
			if self.e != None:
				self.e.rect.centerx = int(ex)
				self.e.rect.bottom = int(ey)
				self.p.points = ppoints
				self.e.points = epoints
			if self.ball != None:
				self.ball.rect.centerx = int(bx)
				self.ball.rect.centery = int(by)
		else:
			components = self.line.split("|")
			pts = components[0]
			ceiling = components[1]
			walls = components[2]
			if ceiling == "True":
				self.ceiling=True
			else:
				self.ceiling=False
			if walls == "True":
				self.walls=True
			else:
				self.walls=False
			self.maxPts = int(pts)

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
		if self.menu.isMenu == True:
			for event in pygame.event.get():
				if event.type == QUIT:
					reactor.stop()
				elif event.type == KEYDOWN:
					if event.key == pygame.K_q:
						reactor.stop()
					elif (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
						if self.value == 1:
							self.menu.changePoints(event.key)
							self.protocol.transport.write(str(event.key))
					elif event.key == pygame.K_c:
						if self.value == 1:
							self.menu.toggleCeilings()
							self.protocol.transport.write(str(event.key))
					elif event.key == pygame.K_w:
						if self.value == 1:
							self.menu.toggleWalls()
							self.protocol.transport.write(str(event.key))
					elif event.key == pygame.K_RETURN:
						self.menu.isMenu = False
						self.protocol.transport.write(str(event.key))

			self.menu.tick()
			self.screen.fill(self.black)
			self.screen.blit(self.menu.image, self.menu.rect)
			self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.title), True, (255,255,255)), ((self.width/4),20))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l2), True, (150,150,255)), ((self.width/8),70))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l3), True, (150,150,255)), ((self.width/8),120))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l4), True, (150,150,255)), ((self.width/8),170))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l6), True, (150,150,255)), ((self.width/8),220))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l5), True, (150,150,255)), ((self.width/8),270))

			pygame.display.flip()
		elif self.menu.isMenu == False and self.gameOver == False:
			for event in pygame.event.get():
				if event.type == QUIT:
					reactor.stop()
				elif event.type == KEYDOWN:
					if event.key == pygame.K_q:
						reactor.stop()
					elif (event.key == pygame.K_a or event.key == pygame.K_d):
						self.protocol.transport.write(str(event.key))
					elif event.key == pygame.K_SPACE:
						self.protocol.transport.write(str(event.key))

			self.screen.fill(self.black)
			if self.p != None:
				self.screen.blit(self.p.image, self.p.rect)
				self.screen.blit(self.e.image, self.e.rect)
				self.screen.blit(self.ball.image, self.ball.rect)
				self.screen.blit(self.net.image, self.net.rect)
				if self.challenge == True:
					self.screen.blit(self.ceiling.image, self.ceiling.rect)

				# red score
				self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.p.points), True, (252,13,27)), ((self.width/4),20))
				# green score
				self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.e.points), True, (42,253,52)), ((3*self.width/4),20))

				# title
				self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.title), True, (255,255,255)), ((5*self.width/16)+15,20))

			pygame.display.flip()
		elif self.gameOver == True:
			for event in pygame.event.get():
				if event.type == QUIT:
					reactor.stop()
				elif event.type == KEYDOWN:
					if event.key == pygame.K_q:
						reactor.stop()
					elif event.key == pygame.K_RETURN:
						self.challenge = True
						self.gameOver = False
						self.ceiling = Ceiling(self)
						self.net = Net(self)
						self.protocol.transport.write(str(event.key))

			self.screen.fill(self.black)
			self.screen.blit(self.endGame.image, self.endGame.rect)
			self.screen.blit(pygame.font.SysFont('mono', 32, bold=True).render(str(self.endGame.winMsg), True, (255,255,255)), ((self.width/8),20))
			self.screen.blit(pygame.font.SysFont('mono', 32, bold=True).render(str(self.endGame.win2), True, (255,255,255)), ((self.width/3),70))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.endGame.loseMsg), True, (150,150,255)), ((self.width/8),170))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.endGame.rMsg), True, (150,150,255)), ((self.width/8),220))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.endGame.qMsg), True, (150,150,255)), ((self.width/8),270))

			pygame.display.flip()

c = Client()

lc = LoopingCall(c.tick)
lc.start(1.0/30)
reactor.connectTCP(SERVER_HOST, SERVER_PORT, ClientFactory(c.new_line))
reactor.run()
lc.stop()
