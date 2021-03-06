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
			
			else:
				if pygame.sprite.collide_rect(self,self.gs.net):
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


			if code == K_RIGHT:
			#	self.rect = self.rect.move(self.mv,0)
				self.vx += self.mv/2
			elif code == K_LEFT:
			#	self.rect = self.rect.move(-self.mv,0)
				self.vx -= self.mv/2
			else:
				pass

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
				#self.x = self.gs.width/4
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
				yDiff = self.gs.p1.by-self.rect.centery#+((xDiff/self.rect.centery) - 5)
				ang = abs(math.atan2(yDiff,xDiff))

				self.vx = math.cos(ang) * -12.5  #self.gs.p1.vx
				self.vx += math.sin(ang)*(1.25*self.gs.p1.vx)
				self.vx += (int(rf*rs))

				if abs(self.vx) < 1:
					self.vx+=random.uniform(-1.5,1.5)

				self.vy *= -0.9
				self.vy -= math.cos(ang)*(0.5*self.gs.p1.vy)
				self.rect = self.rect.move(self.vx,self.vy)

			#bounce from player 2
			elif player == 2:

				xDiff = self.gs.p2.bx-self.rect.centerx
				yDiff = self.gs.p2.by-self.rect.centery#+((xDiff/self.rect.centery) - 5)
				ang = math.atan2(yDiff,xDiff)

				self.vx = math.cos(ang) * -12.5 #self.gs.p1.vx
				self.vx += math.sin(ang)*(1.25*self.gs.p2.vx)
				self.vx += (int(rf*rs))

				if abs(self.vx) < 1:
					self.vx+=random.uniform(-1.5,1.5)

				self.vy *= -0.9
				self.vy -= math.cos(ang)*int(0.5*self.gs.p2.vy)
				self.rect = self.rect.move(self.vx,self.vy)

			#bounce from net
			elif player == 3: #

				if (self.rect.centery >= (self.gs.net.rect.top-5) and self.rect.centery <= (self.gs.net.rect.top+5)):
					self.vy *= int(-0.75)

				else:
					if self.rect.centerx < self.gs.width/2:
						self.rect = self.rect.move(-2,0)
					else:
						self.rect = self.rect.move(2,0)

					self.vx *= -1
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
				if pygame.sprite.collide_rect(self,self.gs.ceiling):
					self.bounce(4)

			#if hits ground
			if self.rect.bottom < self.gs.height-10:
				self.vy += self.gs.ballG
				self.rect = self.rect.move(self.vx,self.vy)

			else: #point awarded sequence
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
			if self.gs.p1.points >= self.gs.maxPts:
				self.win(1)
			elif self.gs.p2.points >= self.gs.maxPts:
				self.win(2)

		def win(self,player):
				self.gs.gameOver = True
				self.gs.endGame = EndGame(player,self.gs)


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
			self.winner = winner
			if self.winner == 1:
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

			self.gs.p1.points = 0
			self.gs.p2.points = 0


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
 
class GameSpace:
	def main(self):
		# initialization
		pygame.init()
		pygame.key.set_repeat(1,50)

		# General Game Variables

		#STAYING CONSTANT
		self.size = self.width, self.height = 640, 480
		self.black = 100, 100, 100 #gray background preferable
		self.count = 0
		self.challenge = False #can only be changed by end game behavior

		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()
		self.g = 0.5
		self.ballG = 0.35
		#game over flag
		self.gameOver = False
		self.quit = False

		self.numPlayers = 1 #default number of players
	
		#CHANGEABLE OBJECTS

		#flags to enable ceilings and walls
		self.ceiling = True
		self.walls = True
		self.maxPts = 25

		self.title = "Slime Volleyball"

		self.menu = Menu(self)

		while self.menu.isMenu == True:

			self.clock.tick(60)

			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					if (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
						self.menu.changePoints(event.key)
					elif event.key == pygame.K_c:
						self.menu.toggleCeilings()
					elif event.key == pygame.K_w:
						self.menu.toggleWalls()
					elif event.key == pygame.K_RETURN:
						self.menu.isMenu = False
					else:
						pass
				else:
					pass


			self.menu.tick()

			self.screen.fill(self.black)

			self.screen.blit(self.menu.image,self.menu.rect)
			self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.title), True, (255,255,255)), ((self.width/4),20))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l2), True, (150,150,255)), ((self.width/8),70))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l3), True, (150,150,255)), ((self.width/8),120))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l4), True, (150,150,255)), ((self.width/8),170))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l6), True, (150,150,255)), ((self.width/8),220))
			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.menu.l5), True, (150,150,255)), ((self.width/8),270))

			pygame.display.flip()


		# set up game objects

		self.p1 = Slime(self,self.numPlayers) #player 1
		self.numPlayers += 1
		self.p2 = Slime(self,self.numPlayers) #player 2 is human
		self.numPlayers += 1

		self.ball = Ball(self)

		self.win = Win(self)

		self.net = Net(self)


		# 3) game loop
		while self.quit == False:
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

			if self.challenge == True:
				self.screen.blit(self.ceiling.image, self.ceiling.rect)

			#displaying red slime score
			self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.p1.points), True, (252,13,27)), ((self.width/4),20))

			#displaying green slime score
			self.screen.blit(pygame.font.SysFont('mono', 36, bold=True).render(str(self.p2.points), True, (42,253,52)), ((3*self.width/4),20))

			self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.title), True, (255,255,255)), ((5*self.width/16)+15,20))


			pygame.display.flip()

			while self.gameOver == True:


				for event in pygame.event.get():

					if event.type == KEYDOWN:
						if event.key == pygame.K_RETURN:
							self.startChallenge()
						elif event.key == pygame.K_q:
							sys.exit()
						else:
							pass
					elif event.type == MOUSEBUTTONDOWN:
						sys.exit()
					elif event.type == QUIT:
						sys.exit()
						pass


				self.screen.fill(self.black)

				self.screen.blit(self.endGame.image,self.endGame.rect)
				self.screen.blit(pygame.font.SysFont('mono', 32, bold=True).render(str(self.endGame.winMsg), True, (255,255,255)), ((self.width/8),20))
				self.screen.blit(pygame.font.SysFont('mono', 32, bold=True).render(str(self.endGame.win2), True, (255,255,255)), ((self.width/3),70))
				self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.endGame.loseMsg), True, (150,150,255)), ((self.width/8),170))
				self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.endGame.rMsg), True, (150,150,255)), ((self.width/8),220))
				self.screen.blit(pygame.font.SysFont('mono', 24, bold=True).render(str(self.endGame.qMsg), True, (150,150,255)), ((self.width/8),270))

				pygame.display.flip()

	def startChallenge(self):
		self.gameOver = False
		self.challenge = True
		self.net = Net(self)
		self.ceiling = Ceiling(self)
		self.ball = Ball(self,self.endGame.winner)


if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
