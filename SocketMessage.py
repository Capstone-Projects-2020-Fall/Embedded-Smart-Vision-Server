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
    # A new stream is trying to connect
    NEW_STREAM = 4


# Used to store message type and data of message
class SocketMessage:
    def __init__(self, message_type: SocketMessageType, data):
        self.message_type = message_type
        self.data = data

    @staticmethod
    def add_node_message(node):
        socket_message = SocketMessage(message_type=SocketMessageType.NEW_NODE,
                                       data=node)
        return socket_message

    # Message detailing adding a stream connection to the server
    @staticmethod
    def add_stream_message(node_name, stream_pipe):
        msg = SocketMessage(message_type=SocketMessageType.NEW_STREAM,
                            data={'node_name': node_name,
                                  'stream_pipe': stream_pipe})
        return msg

    @staticmethod
    def add_video_message(path, tags):
        msg = SocketMessage(message_type=SocketMessageType.UPLOAD,
                            data=(path, tags))
        return msg


# Called to create a message that will send a frame from a node
def create_frame_message(frame: bytearray, node) -> SocketMessage:
    socket_message = SocketMessage(message_type=SocketMessageType.FRAME,
                                   data=(frame, node))
    return socket_message
