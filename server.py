from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

SERVER_HOST = "localhost"
SERVER_PORT = 40025

class ServerConnection(Protocol):

	def __init__(self, addr):
		self.addr = addr

	def dataReceived(self, data):
		print data

	def connectionMade(self):
		print "connection made to %s" % self.addr

	def connectionLost(self, reason):
		print "connection lost to %s" % self.addr

		reactor.stop()

class ServerConnFactory(Factory):

	def __init__(self):
		pass

	def buildProtocol(self, addr):
		return ServerConnection(addr)

#lc = LoopingCall(gameloopiterate)
#lc.start(1.0/60)
reactor.listenTCP(SERVER_PORT, ServerConnFactory())
reactor.run()
#lc.stop()
