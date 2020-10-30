import socket
import os
import struct
from _thread import *
from threading import RLock
from queue import Queue, Empty
import time

from SocketServer.MessageProcessorThread import MessageProcessorThread
from SocketServer.NodeConnection import NodeConnection, NodeStatus
from SocketServer.IncomingThread import IncomingThread

# setup our global variables
from SocketServer.StreamThread import StreamThread
from SocketServer.StreamingNode import StreamingNode

if __name__ == '__main__':
    # Counts our active connections
    active_connections = 0
    # The name of the central server
    central_server_name = "cs-1"
    # The landing spot for all the incoming messages
    inc_messages = Queue()
    # setup our message listener queue
    msg_worker = MessageProcessorThread(inc_messages)
    msg_worker.start()

    # A dictionary to store nodes as well as a lock to broker it's usage
    nc_dict_lock = RLock()
    node_list = {}

    # A dictionary used to store all of the connections for streaming
    str_dict_lock = RLock()
    stream_list = {}


# This thread will broker the connection and exchange details
# Returns a NodeConnection containing all the information
def hand_shake(connection: socket.socket):

    # Send the packed up length of the servers name to the client
    connection.send(
        struct.pack(
            'i',
            len(central_server_name)
        )
    )
    # encode the name of the server to send to the client
    connection.send(
        bytes(
            central_server_name, "utf-8"
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
    print("connection mode:", conn_mode)

    if conn_mode == 0:
        # Create the new node_connection object
        node_connection = NodeConnection(inc_messages)
        # set the name
        node_connection.name = node_name
        # This means this connection is not attempting to be a stream connection
        # set the node connections socket
        node_connection.connection = connection
        # Start the listening threads
        node_connection.start_communication_threads()

        # Set the node connection to active, This should be the last thing to be done
        with nc_dict_lock:
            node_list[node_connection.name] = node_connection
        node_connection.status = NodeStatus.CLIENT_NODE
    elif conn_mode == 1:
        # This is a stream connection so configure it as such
        str_node = StreamingNode()
        str_node.name = node_name
        str_node.stream_thread = StreamThread(node_name, connection)
        str_node.stream_thread.start()
        with str_dict_lock:
            stream_list[node_name] = str_node
        print("Starting socket in stream mode")


# Start a server that listens for new nodes attempting to connect
def start_listening_server():
    # Configure and create the socket
    client_socket = -1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)
    print("\n")

    # Loop around to establish connection while using timeout to allow for interruption
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.bind((socket.gethostname(), 1234))
        s.listen(5)
        print("\n")
        print("Waiting for connection....")
        # Loop around to establish connection while using timeout to allow for interruption
        while True:
            try:
                # Try to accept new connections
                client_socket, address = s.accept()

                # Start a new handshake thread so we can set that up while we wait for another connection
                start_new_thread(hand_shake, (client_socket, ))

            except socket.timeout:
                continue
            print("\nConnection established\n\n")


if __name__ == '__main__':
    start_listening_server()
