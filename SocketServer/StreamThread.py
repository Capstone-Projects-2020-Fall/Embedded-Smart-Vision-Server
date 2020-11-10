# This thread will be spawned and started when a node connects in stream mode
# This class handles all the outgoing traffic and messages
import struct
import threading
import cv2
import pickle
from SocketServer.MessagePack import get_bytes


class StreamThread(threading.Thread):

    def __init__(self, name, connection):
        threading.Thread.__init__(self)
        self.name = name
        self.connection = connection
        self.running = False

    def run(self):
        print("Starting " + self.name)
        self.running = True
        while self.running:
            size_bytes = self.connection.recv(4)
            msg_size = struct.unpack('I', size_bytes)[0]
            raw_data = get_bytes(msg_size, self.connection)

            frame = pickle.loads(raw_data)
            print(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break





