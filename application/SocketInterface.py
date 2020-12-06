from multiprocessing.connection import Connection
import threading

from NodeInformation import NodeInformation
from SocketMessage import SocketMessage, SocketMessageType
from . import video_streams
from application.VideoStream.VideoFeed import VideoStream
from .VideoThread import VideoThread
from application import DBInterface
from application import socketio


class ListeningThread(threading.Thread):
    def __init__(self, connection: Connection):
        threading.Thread.__init__(self)
        self.conn: Connection = connection
        self.running = False
        self.socket_interface: SocketInterface = SocketInterface.getInstance()

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
                        # We want to add a new video to the data base
                        # Unpack our tuple
                        path, tags = message.data
                        # Call out to the database interface to save it
                        DBInterface.add_video(path, tags)

                    elif message.message_type == SocketMessageType.NEW_STREAM:
                        # We have received a new stream to setup
                        node_name = message.data['node_name']
                        stream_pipe = message.data['stream_pipe']
                        self.socket_interface.add_stream(node_name, stream_pipe)
                    else:
                        print("Invalid Socket Message Sent")
                else:
                    print("Unknown Message Recieved!")

    def add_node(self, node_info):
        self.socket_interface.add_node(node_info)

    def update_frame(self, data):
        frame, node = data
        if node in video_streams:
            video_stream: VideoStream = video_streams.get(node)
            video_stream.update_frame(frame)
        else:
            print("Received Message From Unknown Node")


class SocketInterface:
    _instance = None

    # Get the instance of the singleton, if a connection value isn't passed then we are getting
    # an already instantiated instance so we don't need to run the init
    @staticmethod
    def getInstance(connection=None):
        if SocketInterface._instance is None:
            SocketInterface(connection)
        return SocketInterface._instance

    def __init__(self, connection: Connection = None):
        if SocketInterface._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SocketInterface._instance = self

        # Holds the information about connected nodes
        self.connected_nodes = {}

        self.listening_thread = ListeningThread(connection)
        self.listening_thread.start()
        self.socket_server_conn: Connection = connection

    # Add the stream to our version of the node_information
    def add_stream(self, node_name, stream_pipe):
        if node_name in self.connected_nodes:
            # Store the pipe
            self.connected_nodes[node_name].stream_connection = stream_pipe
            video_streams[node_name] = VideoStream()
            self.connected_nodes[node_name].video_camera = video_streams[node_name]
            self.connected_nodes[node_name].video_thread = VideoThread(name=node_name,
                                                                       lf_pipe=stream_pipe,
                                                                       v_feed=video_streams[node_name])
            self.connected_nodes[node_name].video_thread.start()



        else:
            print("Failed to find an active connection for this stream, closing it")

    # Add a node to our information list
    def add_node(self, node_info: NodeInformation):
        self.connected_nodes[node_info.node_name] = node_info

    def remove_node(self):
        pass

    # Returns the stored list of connected nodes
    def get_node_list(self):
        return self.connected_nodes


@socketio.on('frame')
def handle_pulse(node_name):

    SI: SocketInterface = SocketInterface.getInstance()
    if node_name in SI.connected_nodes:
        SI.connected_nodes[node_name].video_thread.pulse_emitter()
