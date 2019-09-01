# Server (Acquisition computer)

import socket
import random


TCP_IP = '127.0.0.1'
TCP_PORT = 50008
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = random.randint(1,10)
    if not data: break
    print "Server will send:", data
    conn.send(data)  # echo
conn.close()




# Client (Stimulation PC)


import sys
from socket import *

TCP_IP = 'localhost'
TCP_PORT = 50008
BUFFER_SIZE = 1024


if len(sys.argv) > 1:
    serverHost = sys.argv[1]

#Create a socket
sSock = socket(AF_INET, SOCK_STREAM)

#Connect to server
sSock.connect((TCP_IP, TCP_PORT))

#Send messages
for item in message:
    #sSock.send(item)
    data = sSock.recv(BUFFER_SIZE)
    print 'Client received: ', 'data'

sSock.close()
