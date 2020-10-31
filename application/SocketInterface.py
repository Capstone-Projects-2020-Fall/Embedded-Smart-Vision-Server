from multiprocessing.connection import Connection
import threading
from SocketMessage import SocketMessage, SocketMessageType
from . import video_streams
from application.VideoStream.VideoFeed import VideoStream


class ListeningThread(threading.Thread):
    def __init__(self, connection: Connection):
        threading.Thread.__init__(self)
        self.conn: Connection = connection
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            # Check if data was sent through the pipe
            if self.conn.poll():
                # Grab the Data and check if it's correct type
                message = self.conn.recv()
                if isinstance(message, SocketMessage):
                    if message.message_type == SocketMessageType.NEW_NODE:
                        print(message.data)
                        self.add_node(message.data)
                    elif message.message_type == SocketMessageType.FRAME:
                        self.update_frame(message.data)
                    elif message.message_type == SocketMessageType.UPLOAD:
                        pass
                    else:
                        print("Invalid Socket Message Sent")
                else:
                    print("Unknown Message Recieved!")

    def add_node(self, data):
        video_streams[data] = VideoStream()

    def update_frame(self, data):
        frame, node = data
        if node in video_streams:
            video_stream: VideoStream = video_streams.get(node)
            video_stream.update_frame(frame)
        else:
            print("Received Message From Unknown Node")


class SocketInterface:
    def __init__(self, connection: Connection):
        self.listening_thread = ListeningThread(connection)
        print("Starting listening thread")
        self.listening_thread.start()
        print("Started listening thread")
        self.socket_server_conn: Connection = connection
