from application import create_app
from multiprocessing import Pipe
from TestStream import TestStream
from application.SocketInterface import SocketInterface
from PIL import Image

if __name__ == '__main__':
    app_conn, socket_conn = Pipe(duplex=True)
    app = create_app()
    socket_interface = SocketInterface(app_conn)
    stream = TestStream(socket_conn)
    stream.start()
    app.run()
