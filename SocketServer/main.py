import socket
import os
import struct
from _thread import *
from queue import Queue, Empty
import time

from MessageProcessorThread import MessageProcessorThread
from NodeConnection import NodeConnection, NodeStatus
from IncomingThread import IncomingThread

# setup our global variables
if __name__ == '__main__':
    # Contains a list of all our nodes
    node_list = []
    # Counts our active connections
    active_connections = 0
    # The name of the central server
    central_server_name = "cs-1"
    # The landing spot for all the incoming messages
    inc_messages = Queue()
    # setup our message listener queue
    msg_worker = MessageProcessorThread(inc_messages)
    msg_worker.start()


# This thread will broker the connection and exchange details
# Returns a NodeConnection containing all the information
def hand_shake(connection: socket.socket, node_connection: NodeConnection):
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
    node_connection.name = connection.recv(
        struct.unpack(
            'i',
            connection.recv(4)
        )[0]).decode("utf-8")
    print(node_connection.name, " Has connected!")

    # set the node connections socket
    node_connection.connection = connection
    # Start the listening threads
    node_connection.start_communication_threads()

    # Set the node connection to active, This should be the last thing to be done
    node_connection.status = NodeStatus.ACTIVE


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
                # A connection is accepted so create a new node connection
                node_conn = NodeConnection(inc_messages)
                # Append this to our list of node connections
                node_list.append(node_conn)
                # Start a new handshake thread so we can set that up while we wait for another connection
                start_new_thread(hand_shake, (client_socket, node_conn,))

            except socket.timeout:
                continue
            print("\nConnection established\n\n")


if __name__ == '__main__':
    start_listening_server()
