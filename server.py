## Multiplayer Slime Volleyball
## Nicholas Jones & Brian Mann
## Twisted/PyGame Project - CSE 30332
## Prof. Collin McMillan


#importing of twisted networking libraries
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import sys
import math #used for calculations
import os
import pygame 
import random #used for randomization in gameplay
from pygame.locals import *

#twisted port details
SERVER_HOST = "localhost"
SERVER_PORT = 40025

class Slime(pygame.sprite.Sprite):
		def __init__(self, gs=None,pn=1,human=True):
			pygame.sprite.Sprite.__init__(self)

			# Member Variable Initialization
			self.gs = gs
			self.pn = pn #player number

			self.human = True #flag for later implementation of a single player mode

			self.points = 0 #player number of points

			self.SpriteScale = 100 #scale for sprites to multiply by
			
			self.ground = self.gs.height #used as quick local variable to calculate boundaries
			
			## initialization differs by player
			if self.pn == 1: #if player 1
				self.image = pygame.image.load("redslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()	
				self.rect.centerx = self.gs.width/4 #initialization location
				self.rect.bottom = self.ground
			elif self.pn == 2: #if player 2
				self.image = pygame.image.load("greenslime.png") #sprite image
				self.image = pygame.transform.scale(self.image,(self.SpriteScale,int(self.SpriteScale*.6)))
				self.rect = self.image.get_rect()
				self.rect.centerx = 3*self.gs.width/4 #initialization location
				self.rect.bottom = self.ground

			self.mv =  8 # constant velocity change (acceleration) added when player is moved
			self.vx = 0 #initial x velocity
			self.vy = 0 #initial y velocity

		#tick function for slime players
		def tick(self):

			#movement series
			if self.rect.bottom > self.ground: #if player is below ground level, bring them up to ground level
				self.rect.bottom = self.ground

			if self.rect.bottom < self.ground: #if player is above ground (in the air)
				if pygame.sprite.collide_rect(self,self.gs.net): #if colliding with net
					if self.pn == 1: #move left if player 1, move right if player 2
						self.vx = -1
					elif self.pn == 2:
						self.vx = 1
				elif self.rect.left <= 0: #if left boundary
					self.vx = 2 #move right quickly
				elif self.rect.right >= self.gs.width: #if right boundary
					self.vx = -2 #move left quickly
				elif self.vx >= 1: #if has velocity rightwards
					self.vx -= 1 #decrease it
				elif self.vx <= -1: #if velocity leftwards
					self.vx += 1 #decrease it
				self.vy += self.gs.g #apply gravity!
				self.rect = self.rect.move(self.vx,self.vy) #apply movement changes

			else: #if player is on ground (no gravity applied)
				if pygame.sprite.collide_rect(self,self.gs.net): #if colliding with net
					if self.pn == 1: #move left if player 1, move right if player 2
						self.vx = -2
					elif self.pn == 2:
						self.vx = 2
				elif self.rect.left <= 0: #if left boundary
						self.vx = 2 #move right quickly
				elif self.rect.right >= self.gs.width: #if right boundary
						self.vx = -2 #move left quickly
				elif self.vx >= 1: #if velocity rightwards
					self.vx -= 1 #decrease it
				elif self.vx <= -1: #if velocity leftwards
					self.vx += 1 #decrease it
				else:
					pass

			self.rect = self.rect.move(self.vx,0) #only apply movement changes along x axis


			#set member tracking varialbes
			self.by = self.rect.bottom 
			self.bx = self.rect.centerx

		def move(self,code):

			# if not computer (always set to human currently)
			if self.human == True:

				#add velocity based on key input
				if code == K_d:
				#	self.rect = self.rect.move(self.mv,0)
					self.vx += self.mv/2
				elif code == K_a:
				#	self.rect = self.rect.move(-self.mv,0)
					self.vx -= self.mv/2
			else: #if computer (mode not implemented)
				self.vx = self.gs.ball.vx


		#jumping function for slime
		def jump(self):

			#if on/around ground
			if (self.rect.bottom <= self.ground) and (self.rect.bottom > self.ground-5):
				self.vy -= 7 #accelerate upwards
				self.rect = self.rect.move(0,self.vy) #apply jumping

#ball class initialization
class Ball(pygame.sprite.Sprite):
		def __init__(self,gs=None,winner=1):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.BallScale = 15 #scaling of image
			self.image = pygame.image.load("ball.png")
			self.image = pygame.transform.scale(self.image,(self.BallScale,self.BallScale))
			self.rect = self.image.get_rect()

			#determines who "serves" based on winner
			if winner == 1:
				self.x = random.randint(self.gs.width/8,(3*self.gs.width/8)) #serve location set to random within boundaries
			else: #if player 2 wins point
				self.x = random.randint((5*self.gs.width/8),(7*self.gs.width/8))
			#self.y = self.gs.height/2
			if self.gs.challenge == False: #if not challenge mode
				self.y = 0 #dropped from top
			else:
				self.y = self.gs.height/4 + 20 #if challenge mode, dropped from lower point
			self.vx = 0
			self.vy = 0
			self.rect.center = (self.x,self.y)


		def bounce(self,player): #bounce function test

			#random factor choices for physics engine
			rf = random.randint(-1,1)
			rs = random.random()

			#bounce from player 1
			if player == 1:
				xDiff = self.gs.p1.bx-self.rect.centerx
				yDiff = self.gs.p1.by-self.rect.centery
				ang = math.atan2(yDiff,xDiff) #calculate angle based on player hit angle

				
				self.vx = math.cos(ang) * -12.5 #x velocity multiplier
				self.vx += math.cos(ang)*self.gs.p1.vx #add portions of player x velocity
				self.vx += (int(rf*rs)) #slight randomness change

				if abs(self.vx) < 1: #if minimal velocity, add randomness to prevent stalemate of ball
					self.vx+=random.uniform(-1.5,1.5)

				self.vy *= -0.9 #decrease y momentum, but sent upwards
				self.vy -= math.cos(ang)*self.gs.p1.vy #add y momentum based on angle
				self.rect = self.rect.move(self.vx,self.vy)

			#bounce from player 2
			elif player == 2:

				xDiff = self.gs.p2.bx-self.rect.centerx
				yDiff = self.gs.p2.by-self.rect.centery
				ang = math.atan2(yDiff,xDiff) #calculate angle based on player hit angle

				self.vx = math.cos(ang) * -12.5 #x velocity multiplier
				self.vx += math.cos(ang)*self.gs.p2.vx #add portions of player x velocity
				self.vx += (int(rf*rs)) #slight randomness change

				if abs(self.vx) < 1: #if minimal velocity, add randomness to prevent stalemate of ball
					self.vx+=random.uniform(-1.5,1.5)

				self.vy *= -0.9 #decrease y momentum, but sent upwards
				self.vy -= math.cos(ang)*self.gs.p2.vy #add y momentum based on angle
				self.rect = self.rect.move(self.vx,self.vy)

			#bounce from net
			elif player == 3:

				if (self.rect.centery >= (self.gs.net.rect.top-5) and self.rect.centery <= (self.gs.net.rect.top+5)): #if top of net
					self.vy *= int(-0.75) #loses y momentum when hits top of net
				else: #if hits net side, bounces quickly backwards
					if self.rect.centerx < self.gs.width/2:
						self.rect = self.rect.move(-2,0)
					else:
						self.rect = self.rect.move(2,0)

			#bounce off ceiling:
			elif player == 4: #no added force
				self.vy *= -1
				self.rect = self.rect.move(self.vx,self.vy)

			#bounces off walls
			elif player == 5: #no added force
				self.vx *= -1
				self.rect = self.rect.move(self.vx,self.vy)


		#ball tick function
		def tick(self):

			# collision detection series
			#chooses bounce function arguments based on who collision is with
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
			elif self.gs.challenge == True: #if hits challenge ceiling
				if pygame.sprite.collide_rect(self, self.gs.ceiling):
					self.bounce(4)

			#testing y value
			if self.rect.bottom < self.gs.height-10: #if does not hit ground
				self.vy += self.gs.ballG #ball gravity
				self.rect = self.rect.move(self.vx,self.vy)

			else: #if hits ground, determine to whom to award the point
				if self.rect.centerx <= self.gs.width/2:
					self.point(2)
				else:
					self.point(1)
					

		#ball has function to "allocate" points
		def point(self,player):

			#function adds a point to winning player and then initializes a new ball to be served on that side

			if player == 1:
				self.gs.p1.points += 1
				self.gs.ball = Ball(gs,1)

			else: #if player is 2
				self.gs.p2.points += 1
				self.gs.ball = Ball(gs,2)


#static net class initialization
class Net(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.NetScale = 100 #transform scaling location
			self.y = self.gs.height-100
			self.image = pygame.image.load("net.png")
			if self.gs.challenge == False: #if not challenge mode, regular size
				self.image = pygame.transform.scale(self.image,(self.NetScale/10,self.NetScale))
			else: #challenge mode causes net height to increase 
				self.image = pygame.transform.scale(self.image,(self.NetScale/10,int(1.5*self.NetScale)))
			self.rect = self.image.get_rect()
			self.rect.centerx = self.gs.width/2
			self.rect.bottom = self.gs.height

#win class checks if game is over and initializes endgame in client
class Win(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			#no real member variables to initialize

		#tick checks for winner and calls win function for either player
		def tick(self):
			if self.gs.p1.points >= self.gs.maxPts:
				self.win(1)
			elif self.gs.p2.points >= self.gs.maxPts:
				self.win(2)
			else:
				pass

		#win function sets gameOver to be true, initializes endgame
		def win(self,player):
			self.gs.gameOver = True

#menu class starts menu before game
class Menu(pygame.sprite.Sprite):
		def __init__(self,gs=None):
			pygame.sprite.Sprite.__init__(self)
			self.gs = gs
			self.image = pygame.image.load("redslime.png") #uses red slime image for display
			self.image = pygame.transform.scale(self.image,(200,120))
			self.rect = self.image.get_rect()
			self.rect.center = (self.gs.width/2,(3*self.gs.height/4)+30)
			self.isMenu = True #self flag variable

			#initialization of menu strings
			self.l2 = "Ceilings are ON. Press 'c' to toggle." 
			self.l3 = "Walls are ON. Press 'w' to toggle."
			self.l4 = "This game is being played to " + str(self.gs.maxPts) + " points,"
			self.l6 = "press the up or down arrows to change."
			self.l5 = "Press ENTER to start!"

		#tick reacts to user inputs to change menu strings
		def tick(self):

			#changing displayed ceiling settings
			if self.gs.ceiling == True:
				self.l2 = "Ceilings are ON. Press 'c' to toggle." 
			else:
				self.l2 = "Ceilings are OFF. Press 'c' to toggle." 

			#changing displayed wall settings
			if self.gs.walls == True:
				self.l3 = "Walls are ON. Press 'w' to toggle."
			else:
				self.l3 = "Walls are OFF. Press 'w' to toggle."

			#changing displayed point settings
			self.l4 = "This game is being played to " + str(self.gs.maxPts) + " points,"


		#modifies points game is played to
		def changePoints(self,code):

			if code == pygame.K_UP:
				self.gs.maxPts += 1
			elif self.gs.maxPts > 1:
				self.gs.maxPts -= 1

		#turns ceilings on and off
		def toggleCeilings(self):
			if self.gs.ceiling == True:
				self.gs.ceiling = False
			else:
				self.gs.ceiling = True

				#turns walls on and off
		def toggleWalls(self):
			if self.gs.walls == True:
				self.gs.walls = False
			else:
				self.gs.walls = True

#static ceiling class initialized in challenge mode
class Ceiling(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.CeilScale = 1000 #set to be very wide to cover all width changes
		self.image = pygame.image.load("ceiling.png")
		self.image = pygame.transform.scale(self.image, (self.CeilScale, 10))
		self.rect = self.image.get_rect()
		self.rect.centerx = self.gs.width/2 #location initialization
		self.rect.centery = self.gs.height/4

class Server(Protocol):

	def __init__(self, players, addr):
		# track number of players
		self.players = players
		self.addr = addr
		# store the gamestate for easier communication to clients
		self.gs = gs
		# store each client's information upon creation in "proxy" class
		if len(self.players) == 0:
			tracker.player1 = self
		elif len(self.players) == 1:
			tracker.player2 = self

	def connectionMade(self):
		# determine which player the client should be
		# first connect is player 1
		if len(self.players) == 0:
			new = 'player_' + str(len(self.players) + 1)
			self.players.append(new)
			self.gs.addplayer(len(self.players))
			print "Player 1 connected!"
			self.transport.write(str(1))
		# second connect is player 2
		elif len(self.players) == 1:
			new = 'player_' + str(len(self.players) + 1)
			self.players.append(new)
			self.gs.addplayer(len(self.players))
			print "Player 2 connected!"
			self.transport.write(str(2))
		# more than two connects is a full server, reject new client
		else:
			self.transport.write("Server is full!")
	def connectionLost(self, reason):
		# determine which client disconnected
		if self == tracker.player1:
			print "Player 1 disconnected!"
			# force other player to disconnect, ending game
			if self.gs.p2 != None:
				tracker.player2.transport.loseConnection()
		elif self == tracker.player2:
			print "Player 2 disconnected!"
			tracker.player1.transport.loseConnection()
		else:
			return
		# reset game state
		self.gs.p1 = None
		self.gs.p2 = None
		self.gs.ball = Ball(self.gs)
		self.gs.net = Net(self.gs)
		self.gs.menu.isMenu = True
		self.gs.enters = 0
		self.gs.maxPts = 25
		self.gs.ceiling = True
		self.gs.walls = True
		self.gs.gameOver = False
		self.gs.challenge = False
		self.players.pop()

	def dataReceived(self, data):
		if self.gs.menu.isMenu == True:
			if data == str(99):
				if self == tracker.player1:
					self.gs.menu.toggleCeilings()
					return
			elif data == str(119):
				if self == tracker.player1:
					self.gs.menu.toggleWalls()
					return
			elif data == str(273):
				if self == tracker.player1:
					key = pygame.K_UP
					self.gs.menu.changePoints(key)
					return
			elif data == str(274):
				if self == tracker.player1:
					key = pygame.K_DOWN
					self.gs.menu.changePoints(key)
					return
			elif data == str(13):
				self.gs.enters += 1
				if self.gs.enters == 2:
					self.gs.menu.isMenu = False
					self.gs.enters = 0
				return
		elif self.gs.gameOver == True:
			if data == str(13):
				self.gs.challenge = True
				self.gs.ball = Ball(self.gs)
				self.gs.ceiling = Ceiling(self.gs)
				self.gs.net = Net(self.gs)
				self.gs.enters += 1
				self.gs.p1.points = 0
				self.gs.p2.points = 0
				if self.gs.enters == 2:
					self.gs.gameOver = False
					self.gs.enters = 0 
		else:
			# determine what key the player's pressed
			if data == str(100):
				key = pygame.K_d
			elif data == str(97):
				key = pygame.K_a
			# if space bar, call jump instead of move
			elif data == str(32):
				if self == tracker.player1:
					self.gs.p1.jump()
					return
				if self == tracker.player2:
					self.gs.p2.jump()
					return
			else:
				return
			# send the specified key to the game state
			if self == tracker.player1:
				self.gs.p1.move(key)
			elif self == tracker.player2:
				self.gs.p2.move(key)

class ServerFactory(Factory):
	# basic Twisted factory
	def __init__(self):
		self.players = []

	def buildProtocol(self, addr):
		return Server(self.players, addr)

class Tracker:
	# proxy class to store which client is which to allow for easier
	# data distribution
	def __init__(self):
		self.player1 = Server
		self.player2 = Server

#gamespace class, encapsulates everything else
class GameSpace:

	#initialization function
	def __init__(self):
		# initialization

		# General Game Variables
		self.size = self.width, self.height = 640, 480

		# Default flags set to start
		self.gameOver = False
		self.maxPts = 25
		self.enters = 0
		self.challenge = False

		#Physics settings
		self.g = 0.5 #slime gravity
		self.ballG = 0.35 #ball gravity

		# initialize game objects
		self.p1 = None
		self.p2 = None
		self.ball = Ball(self)
		self.net = Net(self)
		self.win = Win(self)
		self.ceiling = True
		self.walls = True
		self.menu = Menu(self)

	def addplayer(self, player):
		if player == 1:
			self.p1 = Slime(self, 1)
		else:
			self.p2 = Slime(self, 2)

	#gamespace ticking
	def tick(self):
		if self.menu.isMenu == False and self.gameOver == False:
			if self.ball != None:
				self.ball.tick()
				self.win.tick()
			# make sure there is a client
			if self.p1 != None:
				# update player 1
				self.p1.tick()
				if self.p2 != None:
					# if there's a player 2, update
					# player 1 info over the network about 
					# player 2, as well as the ball
					tracker.player1.transport.write(str(self.p1.rect.centerx)+"|"+str(self.p1.rect.bottom)+"|"+str(self.p2.rect.centerx)+"|"+str(self.p2.rect.bottom)+"|"+str(self.ball.rect.centerx)+"|"+str(self.ball.rect.centery)+"|"+str(self.p1.points)+"|"+str(self.p2.points))
			if self.p2 != None:
				# update player 2
				self.p2.tick()
				# game does not start until two players join,
				# therefore, start ball movement on player 2
				# joining lobby
				# send to player 2 the ball and player 1's info
				tracker.player2.transport.write(str(self.p2.rect.centerx)+"|"+str(self.p2.rect.bottom)+"|"+str(self.p1.rect.centerx)+"|"+str(self.p1.rect.bottom)+"|"+str(self.ball.rect.centerx)+"|"+str(self.ball.rect.centery)+"|"+str(self.p1.points)+"|"+str(self.p2.points))
		elif self.menu.isMenu == True:
			self.menu.tick()
			if self.p2 != None and self.enters == 0:
				tracker.player2.transport.write(str(self.maxPts)+"|"+str(self.ceiling)+"|"+str(self.walls))

		elif self.gameOver == True:
			if self.p1.points >= self.maxPts:
				tracker.player1.transport.write("win1")
				tracker.player2.transport.write("win1")
			elif self.p2.points >= self.maxPts:
				tracker.player1.transport.write("win2")
				tracker.player2.transport.write("win2")
				
tracker = Tracker()
gs = GameSpace()

lc = LoopingCall(gs.tick)
lc.start(1.0/30)
reactor.listenTCP(SERVER_PORT, ServerFactory())
reactor.run()
lc.stop()
