from enum import Enum
from multiprocessing.connection import Connection


# Enumeration for defining the type of message
class SocketMessageType(Enum):
    # New node added
    NEW_NODE = 1
    # Node is sending a live stream frame
    FRAME = 2
    # Node wants to upload to database
    UPLOAD = 3


# Used to store message type and data of message
class SocketMessage:
    def __init__(self, message_type: SocketMessageType, data):
        self.message_type = message_type
        self.data = data


def create_new_node_message(node) -> SocketMessage:
    socket_message = SocketMessage(message_type=SocketMessageType.NEW_NODE,
                                   data=node)
    return socket_message


# Called to create a message that will send a frame from a node
def create_frame_message(frame: bytearray, node) -> SocketMessage:
    socket_message = SocketMessage(message_type=SocketMessageType.FRAME,
                                   data=(frame, node))
    return socket_message
