from multiprocessing import Process, Pipe
from SocketServer.SocketServer import start_socket_server, SocketServer
from multiprocessing import Pipe
from WebDriver import start_webapp
from application.SocketInterface import SocketInterface

if __name__ == '__main__':
    # Create the sockets
    web_app_conn, socket_server_conn = Pipe(duplex=True)

    # Create the socket server process
    socket_server = SocketServer()
    socket_server_proc = Process(target=start_socket_server,
                                 daemon=True, name="Socket_Server",
                                 args=(socket_server,))
    socket_server_proc.run()

    start_webapp(web_app_conn)
