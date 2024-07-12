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

    if args.udp:
        udp_protocol()
    elif args.tcp:
        tcp_protocol()
    else:
        print('Error. Wrong flag')

    logger.info('Finished')

def udp_protocol():
    if args.server:
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(('',  args.server_port))
        print("server is ready")
        if args.file:
            logger.info('Server is ready (socket was created)')

        while 1:
            message, client_address = server_socket.recvfrom(2048)
            modified_message = message.upper()
            print(modified_message)
            print('client address: ', client_address)
            if args.file:
                logger.info('   Message was got. Client address: ' + str (client_address))
            server_socket.sendto(modified_message, client_address)
            server_socket.sendto(bytes(str(client_address) + ' you were connected to the server', "UTF-8"), client_address)

            if message == b'stop':
                if args.file:
                    logger.info('Server process was closed')
                server_socket.close()
                break

    elif args.client:
        client_socket = socket(AF_INET, SOCK_DGRAM)
        print("client is ready")
        if args.file:
            logger.info('Client is ready (socket was created)')
        message = input('input sentence: {write \'stop\' to stop the server process} \n')
        client_socket.sendto(bytes(message, "UTF-8"), ( args.IP_server,  args.server_port))
        if args.file:
                logger.info('   Message was sent')
        modified_sentence, server_address = client_socket.recvfrom(2048)
        address, server_address = client_socket.recvfrom(2048)
        if args.file:
                logger.info('   Answer was got')
        print(modified_sentence)
        print(address)
        client_socket.close()
        if args.file:
                logger.info('Socket was closed')

    else:
        print("Error. Wrong flag")

def tcp_protocol():
    if args.server:
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('',  args.server_port))
        server_socket.listen()
        print("server is ready")
        if args.file:
            logger.info('Server is ready (socket was created)')

        while 1:
            connection_socket, client_address = server_socket.accept()
            if args.file:
                logger.info('   Connection socket was created  (TCP-connection)')
            message = connection_socket.recv(2048)
            modified_message = message.upper()
            print(modified_message)
            print('client address: ', client_address)
            if args.file:
                logger.info('   Answer was got. Client address: ' + str (client_address))

            connection_socket.send(modified_message)
            connection_socket.send(bytes(str(client_address) + ' you were connected to the server', "UTF-8"))
            if args.file:
                logger.info('   Connection socket was closed')
            connection_socket.close()

            if message == b'stop':
                server_socket.close()
                if args.file:
                    logger.info('Server process was closed')
                break

    elif args.client:
        client_socket = socket(AF_INET, SOCK_STREAM)
        if args.file:
            logger.info('Client is ready (socket was created)')
        client_socket.connect(( args.IP_server,  args.server_port))            # tcp-connection
        print("Client is ready")
        if args.file:
                logger.info('   TCP-connection was created')
        message = input('Input sentence: {write \'stop\' to stop the server process} \n')
        client_socket.send(bytes(message, "UTF-8"))
        if args.file:
                logger.info('   Message was sent')
        modified_sentence = client_socket.recv(2048)
        address = client_socket.recv(2048)
        if args.file:
                logger.info('   Answer was got')
        print(modified_sentence)
        print(address)
        client_socket.close()
        if args.file:
                logger.info('Socket was closed')

    else:
        print("Error. Wrong flag")

if __name__ == '__main__':
    main()





