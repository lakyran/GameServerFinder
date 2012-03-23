import sqlite3, struct, socket, time
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class DOTAServerFinder (DatagramProtocol):
    def startProtocol (self):
        pass
    
    def createDatabase (self):
        pass
    
    def serverPinger (self):
        pass
    
    def datagramReceived (self, serverResponse, (host, port)):
        pass


if __name__ == "__main__":
    reactor.listenUDP(0, DOTAServerFinder())
    reactor.run()
