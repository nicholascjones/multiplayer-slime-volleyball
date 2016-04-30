from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import pygame

SERVER_HOST = "localhost"
SERVER_PORT = 40025

class ClientProtocol(LineReceiver):

	def __init__(self, recv):
		self.recv = recv

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
		self.screen = pygame.display.set_mode((200, 200))

	def new_line(self, line):
		self.line = line

	def tick(self):
		self.screen.fill((0,0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				reactor.stop()
		self.screen.blit(pygame.font.SysFont('mono', 12, bold=True).render(self.line, True, (0, 255, 0)), (20,20))
		pygame.display.flip()

if __name__ == '__main__':
	c = Client()

	lc = LoopingCall(c.tick)
	lc.start(1.0/60)
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ClientFactory(c.new_line))
	reactor.run()
	lc.stop()
