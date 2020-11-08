from application import create_app
from multiprocessing import Pipe
from TestStream import TestStream
from application.SocketInterface import SocketInterface
from PIL import Image


def start_webapp(socket_connection):
    app = create_app()
    socket_interface = SocketInterface(connection=socket_connection)
    app.run()
