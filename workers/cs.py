import sqlite3, struct, socket, time
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class CSServerFinder(DatagramProtocol):
    def startProtocol(self):
        self.dbConnection = sqlite3.connect("../db/csdb.sqlite")
        self.dbCursor = self.dbConnection.cursor()
        self.createDatabase()
        self.dstPort = 27015
        self.magicList = [0xff, 0xff, 0xff, 0xff, 0x54, 0x53, 0x6f, 0x75, 0x72, 0x63, 0x65, 0x20, 0x45, 0x6e, 0x67, 0x69, 0x6e, 0x65, 0x20, 0x51, 0x75, 0x65, 0x72, 0x79, 0x00]
        self.magicString = struct.pack("!" + "B"*len(self.magicList), *self.magicList)
        self.ipRanges = ["10.1.33.255", "10.1.34.255", "10.1.35.255", "10.1.36.255", "10.1.39.255", "10.1.40.255",
                         "10.1.65.255", "10.1.66.255", "10.1.98.255", "10.2.12.255", "10.2.16.255", "10.2.20.255",
                         "10.2.24.255", "10.2.28.255", "10.2.32.255", "10.2.36.255", "10.2.4.255" , "10.2.40.244",
                         "10.2.44.255", "10.2.8.255" , "10.3.3.255" , "10.3.4.255" , "10.4.3.255" , "10.5.2.255" ,
                         "172.17.16.255"]
        self.transport.getHandle().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.lastSendTime = None
        self.pingerTask = LoopingCall(self.serverPinger)
        self.pingerTask.start(10.0)
        
    def createDatabase (self):
        try:
            self.dbCursor.execute('drop table if exists cs')
            self.dbCursor.execute('''
               create table cs(
                    serverIP text,
                    serverPort text,
                    serverName text,
                    serverMapName text,
                    serverType text,
                    serverGameName text,
                    serverPlayers int,
                    serverPlayersMax int,
                    serverLatency double)''')
            self.dbConnection.commit()
        except Exception as e:
            print(e)

    def serverPinger (self):
        self.dbCursor.execute('delete from cs')
        self.dbConnection.commit()
        self.lastSendTime = time.time()
        try:
            for self.ipAddr in self.ipRanges:
                self.transport.write(self.magicString, (self.ipAddr, self.dstPort))
        except Exception as e:
                print(e)
                traceback.print_exc()

    def datagramReceived (self, serverResponse, (host, port)):
        serverLatency = int((time.time() - self.lastSendTime)*1000)
        serverResponseList = serverResponse.split("\0")
        serverIP, serverPort = serverResponseList[0].split("m")[1].split(":")
        serverName = serverResponseList[1]
        serverMapName = serverResponseList[2]
        serverType = serverResponseList[3]
        serverGameName = serverResponseList[4]
        serverPlayer = ord(serverResponseList[5][0])
        serverPlayerMax = ord(serverResponseList[5][1])
        
        print ("Server Found" +
               "\n\tServer Name : " + serverName +
               "\n\tServer IP : " + serverIP + ":" + serverPort +
               "\n\tMap Name : " + serverMapName +
               "\n\tType : " + serverType +
               "\n\tPlayers : " + str(serverPlayer) + "/" + str(serverPlayerMax) +
               "\n\tLatency : " + str(serverLatency) + 
               "\n")
        try:
            self.dbCursor.execute("insert into cs values (?,?,?,?,?,?,?,?,?)", (serverIP, serverPort, serverName, serverMapName, serverType, serverGameName, serverPlayer, serverPlayerMax, serverLatency))
            self.dbConnection.commit()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    reactor.listenUDP(56565, CSServerFinder())
    reactor.run()
