# This class handles all the incoming traffic and messages
import pickle
import struct
import threading
from queue import Queue
from socket import socket

import cv2
import numpy as np

from SocketServer.MessagePack import MessagePack, MsgType, get_bytes, Header, build_from_bytes
from SocketServer.QueueMessage import QueueMessage


class IncomingThread(threading.Thread):

    def __init__(self,
                 name: str,
                 inc_queue: Queue,
                 connection: socket):
        """
        :param name:        The name of the thread
        :param inc_queue:   This queue will hold all of the incoming information, we should only be pushing to this
        :param connection:  The socket we are listening on
        """
        # Call the supers init function
        threading.Thread.__init__(self)
        self.name: str = name
        self.running: bool = False
        self.inc_queue: Queue = inc_queue
        self.connection: socket = connection

    def run(self):
        print("Starting: " + self.name)
        self.running = True
        while self.running:
            # Receive the message type
            received_bytes = get_bytes(4, self.connection)
            if len(received_bytes) == 0:
                raise Exception("The other end must have closed")
            # Identify the message type

            msg_type = struct.unpack('i', received_bytes)[0]
            print(msg_type)
            if msg_type == 1:
                print("Handling as test message")
                self.handle_test_message()
            elif msg_type == 2:
                print("Handling as video send")
                self.handle_video_send()
            else:
                print("Message type was not recognized")

        self.break_down()

    def handle_test_message(self):
        # Receive the next four bytes
        received_bytes = get_bytes(4, self.connection)
        # Calculate the length of bytes in the message
        msg_len = struct.unpack('i', received_bytes)[0]
        received_bytes = get_bytes(msg_len, self.connection)
        text = received_bytes.decode('utf-8')
        print("Test command:", text)

    def handle_video_send(self):
        path = "testvid.mp4"
        received_bytes = get_bytes(8, self.connection)
        frame_width, frame_height = struct.unpack('ii', received_bytes)
        out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('a', 'v', 'c', '1'), 10, (frame_width, frame_height))
        while True:
            # Receive the next four bytes
            received_bytes = get_bytes(4, self.connection)
            # Calculate the length of bytes in the message
            msg_len = struct.unpack('i', received_bytes)[0]
            # When we are done sending the video we can just send a negative value to finish the transaction
            if msg_len <= 0:
                break
            received_bytes = get_bytes(msg_len, self.connection)
            img = pickle.loads(received_bytes)
            out.write(img)
        print("Done receiving video")
        out.release()

    def set_running(self, option: bool):
        self.running = option

    def break_down(self):
        print("Breaking down thread: " + self.name)
