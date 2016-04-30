from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

SERVER_HOST = "localhost"
SERVER_PORT = 40025

class ClientConnection(Protocol):

	def __init__(self):
		pass

	def dataReceived(self, data):
		print data

	def connectionMade(self):
		print "connection made to %s port %s" % (SERVER_HOST, SERVER_PORT)

	def connectionLost(self, reason):
		print "connection lost to %s port %s" % (SERVER_HOST, SERVER_PORT)

		reactor.stop()

class ClientConnFactory(ClientFactory):

	def __init__(self):
		pass

	def buildProtocol(self, addr):
		return ClientConnection()

reactor.connectTCP(SERVER_HOST, SERVER_PORT, ClientConnFactory())
reactor.run()
