import sys
import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import select
import pymongo


HOST = ''
SOCKET_LIST = []
RECEIVE_BUFFER = 4096
PORT = 9009


def chat_server():
    server_socket = socket.socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SOCKET_LIST.append(server_socket)

    print 'Chat Server Started on port %s' %(str(PORT))

    while True:
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:

            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print 'Client %s, %s connected' %(addr)

            else:
                try:
                    data = sock.recv(RECEIVE_BUFFER)
                    if data:
                        #there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        #remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        #at this stage if no data likely connection broken
                        broadcast(server_socket, sock, 'Client %s, %s is offline\n'
                                  %(addr))
                except:
                    broadcast(server_socket, sock, 'Client %s, %s is offline\n' %(addr))

    server_socket.close()

def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                #broken socket connection
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == '__main__':
    sys.exit(chat_server())











