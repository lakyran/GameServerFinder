from twisted.internet import reactor

from CSServerFinder import CSServerFinder
from AOEServerFinder import AOEServerFinder
from DOTAServerFinder import DOTAServerFinder

if __name__ == "__main__":
    print ("Staring Servers")
    reactor.listenUDP(0, CSServerFinder())
    reactor.listenUDP(0, DOTAServerFinder())
    reactor.listenUDP(0, AOEServerFinder())   
    reactor.run()
