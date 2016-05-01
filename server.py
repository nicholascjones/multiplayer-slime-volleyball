## Multiplayer Slime Volleyball
## Nicholas Jones & Brian Mann
## Twisted/PyGame Project - CSE 30332
## Prof. Collin McMillan

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

SERVER_HOST = "localhost"
SERVER_PORT = 40025

class Server(LineReceiver):

	def __init__(self, users, players):
		self.users = users
		self.name = None
		self.players = players

	def connectionMade(self):
		new = 'player_' + str(len(self.players) + 1)
		self.players.append(new)
		print "New player connected!"

	def lineReceived(self, line):
		if line == "Number of players?":
			self.sendLine(str(len(self.players)))

class ServerFactory(Factory):

	def __init__(self):
		self.users = {}
		self.players = []

	def buildProtocol(self, addr):
		return Server(self.users, self.players)

reactor.listenTCP(SERVER_PORT, ServerFactory())
reactor.run()
