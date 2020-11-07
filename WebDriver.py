from application import create_app
from multiprocessing import Pipe
from TestStream import TestStream
from application.SocketInterface import SocketInterface
from PIL import Image


def start_webapp():
    app = create_app()
    app.run()
