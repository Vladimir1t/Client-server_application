import socket
import logging
import argparse

logger = logging.getLogger(__name__)

CLIENT_UDP = 0b0101
CLIENT_TCP = 0b0110
SERVER_UDP = 0b1001
SERVER_TCP = 0b1010

def main():
    print("-- Client-server application --")

    args = parse_arguments()

    logging.basicConfig(filename = args.file, level = logging.INFO)
    logger.info('Started')

    callbacks = {
        CLIENT_UDP: client_udp,
        CLIENT_TCP: client_tcp,
        SERVER_UDP: server_udp,
        SERVER_TCP: server_tcp
    }

    callback = callbacks[(args.udp    << 0) |
                         (args.tcp    << 1) |
                         (args.client << 2) |
                         (args.server << 3)]
    print (callback)
    callback(args)

    logger.info('Finished \n')

def parse_arguments():
    parser = argparse.ArgumentParser()

    group_1 = parser.add_mutually_exclusive_group(required = True)
    group_2 = parser.add_mutually_exclusive_group(required = True)
    group_3 = parser.add_mutually_exclusive_group(required = True)

    parser.add_argument("server_IP", type = str)
    parser.add_argument("server_port", type = int)
    group_1.add_argument("-s", "--server", action = 'store_true')
    group_1.add_argument("-c", "--client", action = 'store_true')
    group_2.add_argument("-t", "--tcp", action = 'store_true')
    group_2.add_argument("-u", "--udp", action = 'store_true')
    group_3.add_argument("-f", "--file", action = 'store', type = str, metavar = 'file_log')
    group_3.add_argument("-o", "--stdout", action = 'store_true')

    return parser.parse_args()

def server_udp(args):
    """
    server [-s] uses the UDP transport protocol [-u]
    Server makes socket and listen to the request,
    waits for a message,
    after that sends message to client socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('',  args.server_port))
    logger.info('Server is ready (socket was created)')

    while 1:
        message, client_address = server_socket.recvfrom(2048)
        modified_message = message.upper()
        print(modified_message)
        logger.info('   Message was got. Client address: ' + str (client_address))

        server_socket.sendto(modified_message, client_address)
        server_socket.sendto(bytes(str(client_address) + ' you were connected to the server', "UTF-8"), client_address)

        if message == b'stop':
            logger.info('Server process was closed')
            server_socket.close()
            break

def client_udp(args):
    """
    client [-c] uses the UDP transport protocol [-u]
    Client makes tcp-socket,
    then sends message to server socket and waits for an answer.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logger.info('Client is ready (socket was created)')
    message = input('input sentence: {write \'stop\' to stop the server process} \n')
    client_socket.sendto(bytes(message, "UTF-8"), ( args.server_IP,  args.server_port))
    logger.info('   Message was sent')

    modified_sentence, _ = client_socket.recvfrom(2048)
    address, _ = client_socket.recvfrom(2048)
    logger.info('   Answer was got')
    print(modified_sentence)
    print(address)

    client_socket.close()
    logger.info('Socket was closed')

def server_tcp(args):
    """
    server [-s] uses the TCP transport protocol [-t]
    Server makes socket and listen to the tcp-request,
    then creates connection socket and waits for a message
    after that sends message to client socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('',  args.server_port))
    logger.info('Server is ready (socket was created)')
    server_socket.listen()

    while 1:
        connection_socket, client_address = server_socket.accept()
        logger.info('   Connection socket was created  (TCP-connection)')
        message = connection_socket.recv(2048)
        modified_message = message.upper()
        logger.info('   Answer was got. Client address: ' + str (client_address))

        connection_socket.send(modified_message)
        connection_socket.send(bytes(str(client_address) + ' you were connected to the server', "UTF-8"))
        logger.info('   Connection socket was closed')
        connection_socket.close()

        if message == b'stop':
            server_socket.close()
            logger.info('Server process was closed')
            break

def client_tcp(args):
    """
    client [-c] uses the TCP transport protocol [-t]
    Client makes tcp-socket and starts tcp-connection with server,
    then sends message to server socket and waits for an answer.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.info('Client is ready (socket was created)')
    client_socket.connect((args.server_IP, args.server_port))
    logger.info('   TCP-connection was created')

    message = input('Input sentence: {write \'stop\' to stop the server process} \n')
    client_socket.send(bytes(message, "UTF-8"))
    logger.info('   Message was sent')

    modified_sentence = client_socket.recv(2048)
    address = client_socket.recv(2048)
    logger.info('   Answer was got')

    client_socket.close()
    logger.info('Socket was closed')

if __name__ == '__main__':
    main()





