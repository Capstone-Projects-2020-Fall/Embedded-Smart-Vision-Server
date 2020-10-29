from enum import Enum
from queue import Queue
import socket

from SocketServer.IncomingThread import IncomingThread
from SocketServer.OutgoingThread import OutgoingThread


# Enumeration for defining the current status of the node
class NodeStatus(Enum):
    # Currently establishing connection
    CONNECTING = 1
    # Currently active and functioning
    ACTIVE = 2
    # Currently shutting down the connection
    SHUTTING_DOWN = 3


# This will contain the information needed to define a node
# connection

class NodeConnection:
    def __init__(self, inc_messages):
        # Holds data that needs to be sent
        self.outgoing_queue: Queue = Queue()
        # Holds data the has come in
        self.incoming_queue = inc_messages

        # Holds the incoming threads PID
        self.incoming_thread = -1
        # Holds the outgoing threads PID
        self.outgoing_thread = -1

        # Holds the status the node is currently in
        self.status = NodeStatus.CONNECTING

        # The name of the node
        self.name = "NOT SET"

        # The socket connection for this node
        self.connection = None

    # Starts the communication threads after spawning them
    def start_communication_threads(self):
        # Run a real quick check to make sure we have the socket setup
        if self.connection is None:
            print("ERROR STARTING NODE, ", self.name, ", The socket was never provided!")
        elif not isinstance(self.connection, socket.socket):
            print("ERROR STARTING NODE, ", self.name, ", The provided socket is not a socket")
        else:
            # Since we have the socket start the incoming
            # thread to receive data off the socket
            self.incoming_thread = IncomingThread(self.name,
                                                  self.incoming_queue,
                                                  self.connection)
            # Spin the thread up
            self.incoming_thread.start()
