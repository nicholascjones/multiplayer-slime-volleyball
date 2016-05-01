from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import sys
import math
import os
import pygame
from pygame.locals import *

SERVER_HOST = "localhost"
SERVER_PORT = 40025

class ClientProtocol(LineReceiver):

	def __init__(self, recv):
		self.recv = recv
		c.protocol = self

	def lineReceived(self, line):
		self.recv(line)

class ClientFactory(ClientFactory):

	def __init__(self, recv):
		self.protocol = ClientProtocol
		self.recv = recv

	def buildProtocol(self, addr):
		return ClientProtocol(self.recv)

class Client(object):

	def __init__(self):
		self.line = 'no message'
		pygame.init()
		self.screen = pygame.display.set_mode((600,600))

	def new_line(self, line):
		self.line = line

	def tick(self):
		self.screen.fill((0,0,0))
		for event in pygame.event.get():
			if event.type == QUIT:
				reactor.stop()
			elif event.type == KEYDOWN:
				self.protocol.sendLine(str(event.key))
		self.screen.blit(pygame.font.SysFont('mono', 12, bold=True).render(self.line, True, (0, 255, 0)), (20,20))
		pygame.display.flip()

c = Client()

lc = LoopingCall(c.tick)
lc.start(1.0/60)
reactor.connectTCP(SERVER_HOST, SERVER_PORT, ClientFactory(c.new_line))
reactor.run()
lc.stop()
