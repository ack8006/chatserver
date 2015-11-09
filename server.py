import sys
import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import select


HOST = ''
SOCKET_LIST = []
SOCKET_ALIAS_DICT = {}
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
                setup_for_user_enter(server_socket)

            else:
                try:
                    data = sock.recv(RECEIVE_BUFFER)
                    if data:
                        #there is something in the socket
                        broadcast([server_socket, sock], "\r" + '[' + SOCKET_ALIAS_DICT[sock] + '] ' + data)
                    else:
                        #remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        #at this stage if no data likely connection broken
                        broadcast([server_socket, sock], '\r%s is offline\n'
                                  %(SOCKET_ALIAS_DICT[sock]))
                except:
                    broadcast([server_socket, sock], '\r%s is offline\n'
                                %(SOCKET_ALIAS_DICT[sock]))
                    continue

    server_socket.close()

def setup_for_user_enter(server_socket):
    sockfd, addr = server_socket.accept()
    broadcast_whos_already_in(server_socket, sockfd)
    SOCKET_LIST.append(sockfd)
    print 'Client %s, %s connected' %(addr)
    set_up_username(sockfd)
    broadcast([server_socket, sockfd], '\r%s entered the chat\n'
                %(SOCKET_ALIAS_DICT[sockfd]))


#def broadcast(server_socket, sock, message):
def broadcast(sockets_to_skip, message):
    for socket in SOCKET_LIST:
        #if socket != server_socket and socket != sock:
        if socket not in sockets_to_skip:
            try:
                socket.send(message)
            except:
                #broken socket connection
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

def broadcast_whos_already_in(server_socket, new_sock):
    for socket in SOCKET_LIST:
        if socket != server_socket:
            new_sock.send('\r%s is already in the chat\n'
                          %(SOCKET_ALIAS_DICT[socket]))

def set_up_username(sockfd):
    try:
        username = sockfd.recv(RECEIVE_BUFFER)
        SOCKET_ALIAS_DICT[sockfd] = username
    except:
        #username unable to be received
        print 'username for %s not received, thus closed' %(sockfd)
        sockfd.close()


if __name__ == '__main__':
    sys.exit(chat_server())











