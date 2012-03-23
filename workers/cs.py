import sqlite3
import threading
import socket, struct, time, sys
import traceback

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Echo(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
            serverResponseList = struct.unpack("!" + "B"*len(serverResponse), serverResponse)
            serverPlayerMax = serverPlayer = serverGameName = serverType = serverMapName = serverName = serverPort = serverIP = ""
            i = 5
            while chr(serverResponseList[i]) != ":":
                serverIP += chr(serverResponseList[i])
                i += 1
            i += 1
            while chr(serverResponseList[i]) != "\0":
                serverPort += chr(serverResponseList[i])
                i += 1
            i += 1
            while chr(serverResponseList[i]) != "\0":
                serverName += chr(serverResponseList[i])
                i += 1
            i += 1
            while chr(serverResponseList[i]) != "\0":
                serverMapName += chr(serverResponseList[i])
                i += 1
            i += 1
            while chr(serverResponseList[i]) != "\0":
                serverType += chr(serverResponseList[i])
                i += 1
            i += 1
            while chr(serverResponseList[i]) != "\0":
                serverGameName += chr(serverResponseList[i])
                i += 1
            i += 1
            serverPlayer = serverResponseList[i]
            i += 1
            serverPlayerMax = serverResponseList[i]
                
            print ("Server Found" +
                   "\n\tServer Name : " + serverName +
                   "\n\tServer IP : " + serverIP + ":" + serverPort +
                   "\n\tMap Name : " + serverMapName +
                   "\n\tType : " + serverType +
                   "\n\tPlayers : " + str(serverPlayer) + "/" + str(serverPlayerMax) +
                   "\n")
            dbCursor.execute("insert into cs values (?,?,?,?,?,?,?,?)", (serverIP, serverPort, serverName, serverMapName, serverType, serverGameName, serverPlayer, serverPlayerMax))
            dbConnection.commit()


class CSServerScaner (threading.Thread):
    def __init__ (self):
        self.dstPort = 27015
        self.magicList = [0xff, 0xff, 0xff, 0xff, 0x54, 0x53, 0x6f, 0x75, 0x72, 0x63, 0x65, 0x20, 0x45, 0x6e, 0x67, 0x69, 0x6e, 0x65, 0x20, 0x51, 0x75, 0x65, 0x72, 0x79, 0x00]
        self.magicString = struct.pack("!" + "B"*len(self.magicList), *self.magicList)
        self.ipRanges = ["10.1.33.255", "10.1.34.255", "10.1.35.255", "10.1.36.255", "10.1.39.255", "10.1.40.255",
                         "10.1.65.255", "10.1.66.255", "10.1.98.255", "10.2.12.255", "10.2.16.255", "10.2.20.255",
                         "10.2.24.255", "10.2.28.255", "10.2.32.255", "10.2.36.255", "10.2.4.255" , "10.2.40.244",
                         "10.2.44.255", "10.2.8.255" , "10.3.3.255" , "10.3.4.255" , "10.4.3.255" , "10.5.2.255" ,
                         "172.17.16.255"]
        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sendSocket.bind(("", 56565))
        threading.Thread.__init__(self)

    def run (self):
        self.dbConnection = sqlite3.connect("./csdb.sqlite")
        self.dbCursor = self.dbConnection.cursor()
        while True:
            try:
                self.dbCursor.execute('delete from cs')
                self.dbConnection.commit()
                for self.ipAddr in self.ipRanges:
                    self.sendSocket.sendto(self.magicString, (self.ipAddr, self.dstPort))
                time.sleep(10)
            except Exception as e:
                print (e)
                traceback.print_exc()
                return False


if __name__ == "__main__":
    dbConnection = sqlite3.connect("./csdb.sqlite")
    dbCursor = dbConnection.cursor()
    try:
        dbCursor.execute('drop table if exists cs')
        dbCursor.execute('''
           create table cs(
                serverIP text,
                serverPort text,
                serverName text,
                serverMapName text,
                serverType text,
                serverGameName text,
                serverPlayers int,
                serverPlayersMax int)''')
        dbConnection.commit()
    except Exception as e:
        print (e)
        sys.exit(0)

    bSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bSocket.bind(("", 56565))
    WorkerThread = CSServerScaner()
    WorkerThread.start()


