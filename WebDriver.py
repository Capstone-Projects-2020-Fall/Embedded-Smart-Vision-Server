import os
from application import create_app
from multiprocessing import Pipe
from TestStream import TestStream
from application.SocketInterface import SocketInterface
from PIL import Image


def start_webapp(socket_connection):
    app, socketio = create_app()
    socket_interface = SocketInterface(connection=socket_connection)
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='https://embedded-smart-vision-project.herokuapp.com/', port = port)
