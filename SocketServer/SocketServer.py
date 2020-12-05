import socket
import os
import struct
from _thread import *
from threading import RLock
from queue import Queue, Empty
import time

from DebuggerHost.DebuggerHost import DebuggerHost
from NodeInformation import NodeInformation
from SocketServer.MessageProcessorThread import MessageProcessorThread
from SocketServer.NodeConnection import NodeConnection, NodeStatus
from SocketServer.IncomingThread import IncomingThread

# setup our global variables
from SocketServer.StreamThread import StreamThread
from SocketServer.StreamingNode import StreamingNode
from SocketServer.WebAppInterface import WebAppInterface


class SocketServer:

    def __init__(self, web_app_pipe):
        # Counts our active connections
        self.active_connections = 0
        # The name of the central server
        self.central_server_name = "cs-1"
        # The landing spot for all the incoming messages
        self.inc_messages = Queue()
        # setup our message listener queue
        self.msg_worker = MessageProcessorThread(self.inc_messages)
        self.msg_worker.start()

        # A dictionary to store nodes as well as a lock to broker it's usage
        self.nc_dict_lock = RLock()
        self.node_list = {}

        # A dictionary used to store all of the connections for streaming
        self.str_dict_lock = RLock()
        self.stream_list = {}

        # Create the web app interface
        self.web_interface: WebAppInterface = WebAppInterface.getInstance()
        self.web_interface.set_web_pipe(web_app_pipe)

    # This thread will broker the connection and exchange details
    # Returns a NodeConnection containing all the information
    def hand_shake(self, connection: socket.socket):
        # Send the packed up length of the servers name to the client
        connection.send(
            struct.pack(
                'i',
                len(self.central_server_name)
            )
        )
        # encode the name of the server to send to the client
        connection.send(
            bytes(
                self.central_server_name, "utf-8"
            )
        )
        # Receive and decode the name of the client
        node_name = connection.recv(
            struct.unpack(
                'i',
                connection.recv(4)
            )[0]).decode("utf-8")
        print(node_name, " Has connected!")

        # Read the requested connection mode
        conn_mode = struct.unpack('i', connection.recv(4))[0]

        if conn_mode == 0:
            # Create the new node_connection object
            node_connection = NodeConnection(self.inc_messages)
            # set the name
            node_connection.name = node_name
            # This means this connection is not attempting to be a stream connection
            # set the node connections socket
            node_connection.connection = connection
            # Start the listening threads
            node_connection.start_communication_threads()

            # Set the node connection to active, This should be the last thing to be done
            with self.nc_dict_lock:
                self.node_list[node_connection.name] = node_connection
            node_connection.status = NodeStatus.CLIENT_NODE
            node_info = NodeInformation(node_name=node_name)
            self.web_interface.add_new_node(node_info)

        elif conn_mode == 1:
            # This is a stream connection so configure it as such
            str_thread = StreamThread(node_name, connection)
            str_thread.start()

            with self.nc_dict_lock:
                if node_name in self.node_list:
                    # If the node exists in our node list add it to that stream node
                    self.node_list[node_name].set_stream_node(str_thread)
                else:
                    print("Failed to find an active connection for this stream, closing it")
                    str_thread.running = False
            self.web_interface.setup_stream(node_name, str_thread)

    # Start a server that listens for new nodes attempting to connect
    def start_listening_server(self):
        # Configure and create the socket
        client_socket = -1
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try: 
        s.settimeout(2)
        try:
            port = int(os.environ.get("PORT", 5000))
            s.bind(('0.0.0.0', port))
            s.listen(5)
            print("\n")
        finally:
            print("Server not listening to the socket node")

        # Loop around to establish connection while using timeout to allow for interruption
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            port = int(os.environ.get("PORT", 5000))
            s.bind(('0.0.0.0', port))
            s.listen(5)
            print("\n")
            print("Waiting for connection....")
            # Loop around to establish connection while using timeout to allow for interruption
            while True:
                try:
                    # Try to accept new connections
                    client_socket, address = s.accept()

                    # Start a new handshake thread so we can set that up while we wait for another connection
                    start_new_thread(self.hand_shake, (client_socket,))

                except socket.timeout:
                    continue
                print("\nConnection established\n\n")


def start_socket_server(web_app_con):
    # We are now in a new process with a handle to the socket server
    print("Starting debugger server thread")

    print("Starting socket server")
    socket_server = SocketServer(web_app_con)
    debugger = DebuggerHost(socket_server)
    debugger.start()
    socket_server.start_listening_server()
