import sys
import socket
import select


def chat_client(chat_name):
    if len(sys.argv) < 3:
        print 'Usage: python client.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    #connect to remote host

    try:
        s.connect((host, port))
        #set chat name
        s.send(str(chat_name))
    except:
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. you can send messages now'
    sys.stdout.write('[Me] '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        #get the list socket which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list,[],[])

        for sock in ready_to_read:
            if sock == s:
                #incoming message from remote server, s
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()
            else:
                #user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Me] '); sys.stdout.flush()




if __name__ == '__main__':
    chat_name = raw_input('Please Enter Chat Name ')
    chat_client(chat_name)
    #sys.exit(chat_client())
