from multiprocessing import Process, Pipe

from DebuggerHost.DebuggerHost import DebuggerHost
from SocketServer.SocketServer import start_socket_server, SocketServer
from multiprocessing import Pipe
from WebDriver import start_webapp
from application.SocketInterface import SocketInterface

if __name__ == '__main__':
    # Create the sockets
    web_app_conn, socket_server_conn = Pipe(duplex=True)

    # Create the socket server process

    socket_server_proc = Process(target=start_socket_server,
                                 name="Socket_Server",
                                 args=(web_app_conn, ))

    print('hello')
    socket_server_proc.start()
    print('hello')

    start_webapp(socket_server_conn)

