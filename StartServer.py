from multiprocessing import Process, Pipe
from SocketServer.main import start_socket_server
from multiprocessing import Pipe
from WebDriver import start_webapp

if __name__ == '__main__':
    # Create the sockets
    web_app_conn, socket_server_conn = Pipe(duplex=True)

    # Create the socket server process
    socket_server = Process(target=start_socket_server,
                            daemon=True, name="Socket_Server",
                            args=(socket_server_conn,))
    socket_server.run()

    start_webapp()
