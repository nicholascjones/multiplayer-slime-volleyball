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
		self.sendLine(str(self.players))

class ServerFactory(Factory):

	def __init__(self):
		self.users = {}
		self.players = []

	def buildProtocol(self, addr):
		return Server(self.users, self.players)

reactor.listenTCP(SERVER_PORT, ServerFactory())
reactor.run()
