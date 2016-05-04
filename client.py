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

""" NOTE: MAIN GAME COMMENTS ARE IN SERVER.PY, UNLESS FEATURES DIFFERENTIATE SIGNIFICANTLY (will be noted)"""
"""particularly, the EndGame class is not included in the server program """

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
		# close the game
		c.exit = True

class ClientFactory(ClientFactory):
	# basic Twisted clientfactory
	def __init__(self, recv):
		self.protocol = ClientProtocol
		self.recv = recv

	def buildProtocol(self, addr):
		return ClientProtocol(self.recv)

#slime class
class Slime(pygame.sprite.Sprite):
		def __init__(self, gs=None,pn=1,human=True):
			pygame.sprite.Sprite.__init__(self)

			# Member Variable Initialization
			self.gs = gs
			self.pn = pn #player number

			self.human = True

			#initialized points to zero
			self.points = 0 #player number of points

			self.SpriteScale = 100 #scale for sprites to multiply by
			
			self.ground = self.gs.height
			
			## initialization differs by player
			if self.pn == 1:
				self.image = pygame.image.load("redslime.png") #red sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()	
				self.rect.centerx = self.gs.width/4 #location initialized
				self.rect.bottom = self.ground
			elif self.pn == 2:
				self.image = pygame.image.load("greenslime.png") #green sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()
				self.rect.centerx = 3*self.gs.width/4 #location initialized
				self.rect.bottom = self.ground

			self.mv =  8 # velocity used 
			self.vx = 0 #initial x velocity
			self.vy = 0 #initial y velocity

#ball class
class Ball(pygame.sprite.Sprite):
		def __init__(self,gs=None,winner=1):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.BallScale = 15 #transformation scale
			self.image = pygame.image.load("ball.png")
			self.image = pygame.transform.scale(self.image,(self.BallScale,self.BallScale))
			self.rect = self.image.get_rect()

			#determines who "serves" based on winner of last point
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
			self.rect.center = (self.x,self.y) #initial location set

		#function to award points based on where ball lands
		def point(self,player):

			if player == 1:
				self.gs.p1.points += 1
				self.gs.ball = Ball(gs,1)

			else: #if player is 2
				self.gs.p2.points += 1
				self.gs.ball = Ball(gs,2)

#static net class, main comments in server
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

#win class ticks to determine if game is over, and subsequently decides endgame sequence
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

		#winning initializes EndGame based on player
		def win(self,player):
				self.gs.gameOver = True
				self.gs.endGame = EndGame(player, self.gs)

#pre-game menu for changing of settings--commented in server.py
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


			# change number of points game is played to
		def changePoints(self,code):

			if code == pygame.K_UP:
				self.gs.maxPts += 1
			elif self.gs.maxPts > 1:
				self.gs.maxPts -= 1

				#turn ceilings on and off
		def toggleCeilings(self):
			if self.gs.ceiling == True:
				self.gs.ceiling = False
			else:
				self.gs.ceiling = True

				#turn walls on and off
		def toggleWalls(self):
			if self.gs.walls == True:
				self.gs.walls = False
			else:
				self.gs.walls = True

#EndGame class comes up when a game ends		
class EndGame(pygame.sprite.Sprite):
		def __init__(self,winner,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			if winner == 1: #if player 1 wins, display as such
				self.image = pygame.image.load("redslime.png")
				self.winMsg = "Congratulations, Player 1!"
				self.loseMsg = "Player 2...better luck next time!"
			else: #if player 2 wins, display as such
				self.image = pygame.image.load("greenslime.png")
				self.winMsg = "Congratulations, Player 2"
				self.loseMsg = "Player 1...better luck next time!"

			self.win2 = "YOU WIN!" #string setting
			self.image = pygame.transform.scale(self.image,(200,120)) #display winning slime
			self.rect = self.image.get_rect()
			self.rect.center = (self.gs.width/2,(3*self.gs.height/4)+30)
			self.rMsg = "To play a CHALLENGE GAME, press ENTER"
			self.qMsg = "To quit, press the 'q' key."
			self.gameOver = True

			self.gs.p.points = 0 #reset points back to zero
			self.gs.e.points = 0

#static ceiling class for in challenge mode, drops lower than normal ceiling and
#displays as white
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
		# game variables and other variables needed to manage
		# the game and the client's connection
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
		# did a client win
		if self.line == "win1":
			self.win.win(1)
		elif self.line == "win2":
			self.win.win(2)
		# intial connection information, such as which player
		# the client is by running connectionMade
		if self.connected == False and (self.line == str(1) or self.line == str(2) or self.line == "Server is full!"):
			self.connected = True
			self.connectionMade()
			return
		# data for when the game has started
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
			# update player's info
			if self.p != None:
				self.p.rect.centerx = int(px)
				self.p.rect.bottom = int(py)
			# update enemy's info
			if self.e != None:
				self.e.rect.centerx = int(ex)
				self.e.rect.bottom = int(ey)
			# update points
				self.p.points = ppoints
				self.e.points = epoints
			# update ball
			if self.ball != None:
				self.ball.rect.centerx = int(bx)
				self.ball.rect.centery = int(by)
		# data for menu mode
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
		# menu mode
		#handling user input in menu 
		if self.menu.isMenu == True: #set menu flag to be true
			for event in pygame.event.get():
				if event.type == QUIT:
					reactor.stop()
				elif event.type == KEYDOWN:
					if event.key == pygame.K_q:
						reactor.stop()
					# change point totals
					elif (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
						if self.value == 1:
							self.menu.changePoints(event.key)
							self.protocol.transport.write(str(event.key))
					# toggle ceilings
					elif event.key == pygame.K_c:
						if self.value == 1:
							self.menu.toggleCeilings()
							self.protocol.transport.write(str(event.key))
					# toggle walls
					elif event.key == pygame.K_w:
						if self.value == 1:
							self.menu.toggleWalls()
							self.protocol.transport.write(str(event.key))
					# start the game
					elif event.key == pygame.K_RETURN:
						self.menu.isMenu = False
						self.protocol.transport.write(str(event.key))
			# fill the screen
			self.menu.tick()
			self.screen.fill(self.black)
			self.screen.blit(self.menu.image, self.menu.rect)
			## display menu items
			self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.title), True, (255,255,255)), ((self.width/4),20))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l2), True, (150,150,255)), ((self.width/8),70))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l3), True, (150,150,255)), ((self.width/8),120))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l4), True, (150,150,255)), ((self.width/8),170))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l6), True, (150,150,255)), ((self.width/8),220))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l5), True, (150,150,255)), ((self.width/8),270))

			pygame.display.flip()
		# gameplay mode

		#if have moved into gameplay mode, take inputs
		elif self.menu.isMenu == False and self.gameOver == False:
			for event in pygame.event.get():
				if event.type == QUIT:
					reactor.stop()
				elif event.type == KEYDOWN:
					if event.key == pygame.K_q:
						reactor.stop()
					# movement keys
					elif (event.key == pygame.K_a or event.key == pygame.K_d):
						self.protocol.transport.write(str(event.key))
					# jumping
					elif event.key == pygame.K_SPACE:
						self.protocol.transport.write(str(event.key))

			self.screen.fill(self.black)
			# update the screen
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
		# post game menu
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
			# update the screen
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
