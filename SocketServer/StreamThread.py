# This thread will be spawned and started when a node connects in stream mode
# This class handles all the outgoing traffic and messages
import struct
import threading
import pickle

import cv2

from SocketServer.MessagePack import get_bytes


class StreamThread(threading.Thread):

    def __init__(self, name, connection):
        threading.Thread.__init__(self)
        self.name = name
        self.connection = connection
        self.running = False
        self.web_pipe = None

    def run(self):
        print("Starting " + self.name + " which is a StreamThread")
        self.running = True
        while self.running:
            size_bytes = self.connection.recv(4)
            msg_size = struct.unpack('I', size_bytes)[0]
            raw_data = get_bytes(msg_size, self.connection)
            # Unpickle the raw data we received
            frame = pickle.loads(raw_data)
            # Send it down the web pipe after verifying our pipe is set
            if self.web_pipe is not None:
                self.web_pipe.send(frame)
        self.break_down()

    def set_web_pipe(self, web_pipe):
        print("Setting web pipe in stream thread")
        self.web_pipe = web_pipe

    def break_down(self):
        print("Breaking down stream thread")
        self.connection.close()
