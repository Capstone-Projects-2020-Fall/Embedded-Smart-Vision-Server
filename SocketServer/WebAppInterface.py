from multiprocessing.connection import Connection, Pipe

from NodeInformation import NodeInformation
from SocketMessage import SocketMessage


# This class is a singleton method that allows for a simple interface for interacting with and talking to the web
# portal
class WebAppInterface:
    _instance = None

    @staticmethod
    def getInstance():
        if WebAppInterface._instance is None:
            WebAppInterface()
        return WebAppInterface._instance

    def __init__(self):
        if WebAppInterface._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            WebAppInterface._instance = self

        # Holds the information about connected nodes
        self.connected_nodes = {}
        self.web_app_pipe = None

    def set_web_pipe(self, web_app_pipe):
        self.web_app_pipe = web_app_pipe

    # Take in a new node and set it's name
    def add_new_node(self, node_info: NodeInformation):
        self.connected_nodes[node_info] = node_info
        msg = SocketMessage.add_node_message(node_info)
        self.web_app_pipe.send(msg)

    def remove_node(self):
        pass

    def setup_stream(self, node_name, stream_thread):
        print("WebAppInterface is calling setup stream")
        # Create new pipe to link up the stream thread
        h, c = Pipe(duplex=True)
        msg = SocketMessage.add_stream_message(node_name, c)
        stream_thread.set_web_pipe(h)
        self.web_app_pipe.send(msg)

    def add_video_data(self, video_path, tags):
        print("WebAppInterface - adding video to DB", video_path, tags)
        msg = SocketMessage.add_video_message(video_path, tags)
        self.web_app_pipe.send(msg)

    def disconnect_stream(self):
        pass
