import sys
from socket import *

def udp_protocol (mode):
    if flag_1 == '-s':
        server_socket = socket (AF_INET, SOCK_DGRAM)
        server_socket.bind (('', server_port))
        print ("server is ready")
        if mode == 'f':
            file.write ('Server is ready (socket was created) \n')

        while 1:
            message, client_address = server_socket.recvfrom (2048)
            modified_message = message.upper ()
            print (modified_message)
            print ('client address: ', client_address)
            if mode == 'f':
                file.write ('   Message was got. Client address: ' + str (client_address) + '\n')
            server_socket.sendto (modified_message, client_address)
            server_socket.sendto (bytes(str(client_address) + ' you were connected to the server', "UTF-8"), client_address)

            if message == b'stop':
                if mode == 'f':
                    file.write ('Server process was closed \n')
                server_socket.close ()
                break

    elif flag_1 == '-c':
        client_socket = socket (AF_INET, SOCK_DGRAM)
        print ("client is ready")
        if mode == 'f':
            file.write ('Client is ready (socket was created) \n')
        message = input ('input sentence: {write stop to stop the server process}\n')
        client_socket.sendto (bytes(message, "UTF-8"), (IP_server, server_port))
        if mode == 'f':
                file.write ('   Message was sent \n')
        modified_sentence, server_address = client_socket.recvfrom (2048)
        address, server_address = client_socket.recvfrom (2048)
        if mode == 'f':
                file.write ('   Answer was got \n')
        print (modified_sentence)
        print (address)
        client_socket.close ()
        if mode == 'f':
                file.write ('Socket was closed \n')

    else:
        print ("Error. Wrong flag")

def tcp_protocol (mode):
    if flag_1 == '-s':
        server_socket = socket (AF_INET, SOCK_STREAM)
        server_socket.bind (('', server_port))
        server_socket.listen ()
        print ("server is ready")
        if mode == 'f':
            file.write ('Server is ready (socket was created) \n')

        while 1:
            connection_socket, client_address = server_socket.accept ()
            if mode == 'f':
                file.write ('   Connection socket was created  (TCP-connection) \n')
            message = connection_socket.recv (2048)
            modified_message = message.upper ()
            print (modified_message)
            print ('client address: ', client_address)
            if mode == 'f':
                file.write ('   Answer was got. Client address: ' + str (client_address) + '\n')

            connection_socket.send (modified_message)
            connection_socket.send (bytes(str(client_address) + ' you were connected to the server', "UTF-8"))
            if mode == 'f':
                file.write ('   Connection socket was closed \n')
            connection_socket.close ()

            if message == b'stop':
                server_socket.close ()
                if mode == 'f':
                    file.write ('Server process was closed \n')
                break

    elif flag_1 == '-c':
        client_socket = socket (AF_INET, SOCK_STREAM)
        if mode == 'f':
            file.write ('Client is ready (socket was created) \n')
        client_socket.connect ((IP_server, server_port))            # tcp-connection
        print ("Client is ready")
        if mode == 'f':
                file.write ('   TCP-connection was created \n')
        message = input ('Input sentence: {write \'stop\' to stop the server process}\n')
        client_socket.send (bytes(message, "UTF-8"))
        if mode == 'f':
                file.write ('   Message was sent \n')
        modified_sentence = client_socket.recv (2048)
        address = client_socket.recv (2048)
        if mode == 'f':
                file.write ('   Answer was got \n')
        print (modified_sentence)
        print (address)
        client_socket.close ()
        if mode == 'f':
                file.write ('Socket was closed \n')

    else:
        print ("Error. Wrong flag")

print ("-- Client-server application --")

IP_server   = str(sys.argv[1])
server_port = int(sys.argv[2])
flag_1      = str(sys.argv[3])
flag_2      = str(sys.argv[4])
flag_3      = str(sys.argv[5])
file_log    = str(sys.argv[6])

file = open (file_log, 'w')

if flag_3 == '-f':
    mode = 'f'
elif flag == '-o':
    mode = 'o'

if flag_2 == '-u':
    udp_protocol (mode)
elif flag_2 == '-t':
    tcp_protocol (mode)
else:
    print ('Error. Wrong flag')

file.close ()




