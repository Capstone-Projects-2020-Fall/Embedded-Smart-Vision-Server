import cv2 as cv
from multiprocessing.connection import Connection
#from SocketMessage import SocketMessage, SocketMessageType, create_new_node_message, create_frame_message
import threading


class TestStream(threading.Thread):
    def __init__(self, conn: Connection):
        threading.Thread.__init__(self)
        self.conn: Connection = conn
        self.running = False

    def run(self) -> None:
        self.running = True
        node_message = create_new_node_message('node')
        print("Created Message to add node:", node_message)
        self.conn.send(node_message)
        print("Reading Image")
        test_image = cv.imread('TestPhoto.jpg')
        print("Read Image")
        success, to_send = cv.imencode('.jpg', test_image)
        frame_message = create_frame_message(to_send.tobytes(), 'node')
        print("Created Message to add update frame:", node_message)
        while self.running:
            cv.imshow('Frame', test_image)
            self.conn.send(frame_message)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
