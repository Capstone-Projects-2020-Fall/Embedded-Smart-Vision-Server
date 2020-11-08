# a host we can connect into to debug code
import struct
import threading
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM, gethostname, timeout
from SocketServer.MessagePack import MessagePack, MsgType, get_bytes, Header, build_from_bytes
from SocketServer.QueueMessage import QueueMessage


class DebuggerHost(threading.Thread):

    def __init__(self, socket_server):

        # Call the supers init function
        threading.Thread.__init__(self)
        self.running = False
        self.socket_server= socket_server

    def run(self):
        print("Starting debugger thread")
        self.running = True
        # Setup socket
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(2)
        sock.bind((gethostname(), 555))
        sock.listen(5)
        client_socket, address = None, None
        while True:
            try:
                client_socket, address = sock.accept()
            except timeout:
                continue
            print("Debugger connected!")
            break

        while self.running:
            # receive the message bytes
            msg_bytes = client_socket.recv(1024)
            # Decode the message
            msg = msg_bytes.decode("utf-8")

            # Do reply stuff here
            if msg == 'getNodeList':
                print(self.socket_server.node_list)

        self.break_down()

    def set_running(self, option: bool):
        self.running = option

    def break_down(self):
        print("Breaking down thread: " + self.name)
