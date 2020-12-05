import os
from application import create_app
from multiprocessing import Pipe
from TestStream import TestStream
from application.SocketInterface import SocketInterface
from PIL import Image


def start_webapp():
    app, socketio = create_app()
    # socket_interface = SocketInterface(connection=socket_connection)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port = port)
