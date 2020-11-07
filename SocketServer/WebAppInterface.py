from multiprocessing.connection import Connection


class SocketInterface:
    _instance = None

    @staticmethod
    def getInstance():
        if SocketInterface._instance is None:
            SocketInterface()
        return SocketInterface._instance

    def __init__(self, connection: Connection):
        if SocketInterface._instance != None:
            raise Exception("This class is a singleton!")
        else:
            SocketInterface._instance = self

        # Holds the information about connected nodes
        self.connected_nodes = None

    def add_new_node(self):
        pass

    def remove_node(self):
        pass

    def setup_stream(self):
        pass

    def disconnect_stream(self):
        pass
