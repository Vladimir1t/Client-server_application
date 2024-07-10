import sys
from socket import *
from threading import Thread
import threading
import os

print ("-- Client-server application --")

IP_server   = str(sys.argv[1])
server_port = int(sys.argv[2])
flag_1      = str(sys.argv[3])
flag_2      = str(sys.argv[4])
flag_3      = str(sys.argv[5])
file_log    = str(sys.argv[6])

if flag_1 == '-s':
    server_socket = socket (AF_INET, SOCK_DGRAM)
    server_socket.bind (('', server_port))
    print ("server is ready")
    while 1:
        message, client_address = server_socket.recvfrom (2048)
        modified_message = message.upper ()
        print (modified_message)
        print ('client address: ', client_address)
        server_socket.sendto (modified_message, client_address)
        server_socket.sendto (bytes(str(client_address), "UTF-8"), client_address)

elif flag_1 == '-c':
    client_socket = socket (AF_INET, SOCK_DGRAM)
    print ("client is ready")
    message = input ('input sentence: ')
    # client_socket.connect ((IP_server, server_port))
    client_socket.sendto (bytes(message, "UTF-8"), (IP_server, server_port))
    modified_sentence, server_address = client_socket.recvfrom (2048)
    address, server_address = client_socket.recvfrom (2048)
    print (modified_sentence)
    print (address)
    client_socket.close ()

else:
    print ("Error. Wrong flag")




