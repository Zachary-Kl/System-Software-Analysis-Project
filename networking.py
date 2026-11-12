# networking things

from twisted.protocols import basic
from twisted.application import internet, service
from twisted.internet import protocol


class Client(basic.LineReceiver):
    def connectionMade(self):
        print("Got new client!")
        self.factory.clients.append(self)
        for c in self.factory.clients:
            c.message(("You have been connected").encode('ASCII'))

    def connectionLost(self, reason):
        print("Lost a client!")
        self.factory.clients.remove(self)

    def lineReceived(self, line): # testing for now, eventually will be data driven with json
        print("received", line)
        for c in self.factory.clients:
            c.message(line)

    def message(self, message):
        self.transport.write(message + b"\n")


# testing here!

# run twistd -y networking.py
factory = protocol.ServerFactory() # create server factory
factory.protocol = Client # set the protocol to be routed through client
factory.clients = [] # make a list of clients
application = service.Application("server") # create application
internet.TCPServer(1025, factory).setServiceParent(application) # finally open the port and application