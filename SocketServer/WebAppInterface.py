from multiprocessing.connection import Connection

from NodeInformation import NodeInformation
from SocketMessage import SocketMessage


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

    # Take in a new node a set it's name
    def add_new_node(self, node_info: NodeInformation):
        print("Web app interface: Adding new node")
        self.connected_nodes[node_info] = node_info
        msg = SocketMessage.add_node_message(node_info)
        self.web_app_pipe.send(msg)

    def remove_node(self):
        pass

    def setup_stream(self):
        pass

    def disconnect_stream(self):
        pass
