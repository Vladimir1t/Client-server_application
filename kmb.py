import sys
from socket import *
import logging
logger = logging.getLogger(__name__)
import argparse
parser = argparse.ArgumentParser()
group_1 = parser.add_mutually_exclusive_group(required=True)
group_2 = parser.add_mutually_exclusive_group(required=True)
group_3 = parser.add_mutually_exclusive_group(required=True)

parser.add_argument("IP_server", type = str)
parser.add_argument("server_port", type = int)
group_1.add_argument("-s", "--server", action = 'store_true')
group_1.add_argument("-c", "--client", action = 'store_true')
group_2.add_argument("-t", "--tcp", action = 'store_true')
group_2.add_argument("-u", "--udp", action = 'store_true')
group_3.add_argument("-f", "--file", action = 'store', type = str, metavar = 'file_log')
group_3.add_argument("-o", "--o")

args = parser.parse_args()

def main():
    print("-- Client-server application --")

    logging.basicConfig(filename = args.file, level = logging.INFO)
    logger.info('Started')

    if args.file:
        mode = 'f'
    elif args.o:
        mode = 'o'

    if args.udp:
        udp_protocol(mode)
    elif args.tcp:
        tcp_protocol(mode)
    else:
        print('Error. Wrong flag')

    logger.info('Finished')

def udp_protocol(mode):
    if args.server:
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(('',  args.server_port))
        print("server is ready")
        if mode == 'f':
            logger.info('Server is ready (socket was created) \n')

        while 1:
            message, client_address = server_socket.recvfrom(2048)
            modified_message = message.upper()
            print(modified_message)
            print('client address: ', client_address)
            if mode == 'f':
                logger.info('   Message was got. Client address: ' + str (client_address) + '\n')
            server_socket.sendto(modified_message, client_address)
            server_socket.sendto(bytes(str(client_address) + ' you were connected to the server', "UTF-8"), client_address)

            if message == b'stop':
                if mode == 'f':
                    logger.info('Server process was closed \n')
                server_socket.close()
                break

    elif args.client:
        client_socket = socket(AF_INET, SOCK_DGRAM)
        print("client is ready")
        if mode == 'f':
            logger.info('Client is ready (socket was created) \n')
        message = input('input sentence: {write stop to stop the server process}\n')
        client_socket.sendto(bytes(message, "UTF-8"), ( args.IP_server,  args.server_port))
        if mode == 'f':
                logger.info('   Message was sent \n')
        modified_sentence, server_address = client_socket.recvfrom(2048)
        address, server_address = client_socket.recvfrom(2048)
        if mode == 'f':
                logger.info('   Answer was got \n')
        print(modified_sentence)
        print(address)
        client_socket.close()
        if mode == 'f':
                logger.info('Socket was closed \n')

    else:
        print("Error. Wrong flag")

def tcp_protocol(mode):
    if args.server:
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('',  args.server_port))
        server_socket.listen()
        print("server is ready")
        if mode == 'f':
            logger.info('Server is ready (socket was created) \n')

        while 1:
            connection_socket, client_address = server_socket.accept()
            if mode == 'f':
                logger.info('   Connection socket was created  (TCP-connection) \n')
            message = connection_socket.recv(2048)
            modified_message = message.upper()
            print(modified_message)
            print('client address: ', client_address)
            if mode == 'f':
                logger.info('   Answer was got. Client address: ' + str (client_address) + '\n')

            connection_socket.send(modified_message)
            connection_socket.send(bytes(str(client_address) + ' you were connected to the server', "UTF-8"))
            if mode == 'f':
                logger.info('   Connection socket was closed \n')
            connection_socket.close()

            if message == b'stop':
                server_socket.close()
                if mode == 'f':
                    logger.info('Server process was closed \n')
                break

    elif args.client:
        client_socket = socket(AF_INET, SOCK_STREAM)
        if mode == 'f':
            logger.info('Client is ready (socket was created) \n')
        client_socket.connect(( args.IP_server,  args.server_port))            # tcp-connection
        print("Client is ready")
        if mode == 'f':
                logger.info('   TCP-connection was created \n')
        message = input('Input sentence: {write \'stop\' to stop the server process}\n')
        client_socket.send(bytes(message, "UTF-8"))
        if mode == 'f':
                logger.info('   Message was sent \n')
        modified_sentence = client_socket.recv(2048)
        address = client_socket.recv(2048)
        if mode == 'f':
                logger.info('   Answer was got \n')
        print(modified_sentence)
        print(address)
        client_socket.close()
        if mode == 'f':
                logger.info('Socket was closed \n')

    else:
        print("Error. Wrong flag")

if __name__ == '__main__':
    main()





