# This class handles all the incoming traffic and messages
import os
import pickle
import struct
import threading
from queue import Queue
from socket import socket
from datetime import datetime
import cv2

from SocketServer.ByteStreamAdapter import bs_adapter
from SocketServer.WebAppInterface import WebAppInterface

lbl = "Incoming Thread - "


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
        # Create a byte stream adapter for easier use
        self.bsa = bs_adapter(self.connection)

    def run(self):
        print("Starting: " + self.name)
        self.running = True
        while self.running:
            # Receive the message type
            received_bytes = self.bsa.get_bytes(4)
            if len(received_bytes) == 0:
                raise Exception(lbl, "The other end must have closed")
            # Identify the message type

            msg_type = struct.unpack('i', received_bytes)[0]
            print(msg_type)
            if msg_type == 1:
                print(lbl, "Handling as test message")
                self.handle_test_message()
            elif msg_type == 2:
                print(lbl, "Handling as video send")
                self.handle_video_send()
            else:
                print(lbl, "Message type was not recognized")

        self.break_down()

    def handle_test_message(self):
        # Receive the next four bytes
        received_bytes = self.bsa.get_bytes(4)
        # Calculate the length of bytes in the message
        msg_len = struct.unpack('i', received_bytes)[0]
        received_bytes = self.bsa.get_bytes(msg_len)
        text = received_bytes.decode('utf-8')
        print(lbl, "Test command:", text)

    def handle_video_send(self):
        path, video_title = self.generate_video_path()
        received_tags = []

        # Create local copy of bsa
        _bsa = self.bsa
        ### Receive file check ###
        file_check = _bsa.read_int()
        print(lbl, "File check result: ", file_check)
        if file_check != 1:
            # Verify the node wants to continue the transaction, if not return early
            print(lbl, "The node failed to open the file and aborted the transaction")
            return
        else:
            print(lbl, "The node opened the file successfully and will now continue")

        ### Receive tag count ###
        tag_count = _bsa.read_int()
        print(lbl, "Receiving", tag_count, "tags")

        # Per tag #
        # Check to make sure there are actually tags to receive
        while tag_count > 0:
            ### Receive the length of the first tag ###
            tag_len = _bsa.read_int()

            if tag_len <= 0:
                # Check if we have received an end of tag message
                print(lbl, "Done reading tags")
                break

            ### Receive tag string ###
            tag_str = _bsa.read_string(tag_len)
            received_tags.append(tag_str)
            print(lbl, "Received tag:", tag_str, "at", tag_count)
            # Keep track of how many more tags we need to read
            tag_count -= 1

        if tag_count == 0:
            # If we successfully read all our tags
            # We need to consume the end of tags message
            ### Read tags done message ###
            tag_res = _bsa.read_int()
            print(lbl, "Finished reading tags successfully:", tag_res)

        ### Read frame count ###
        frame_count = _bsa.read_int()
        ### Read frame width ###
        frame_width = _bsa.read_int()
        ### Read frame Height ###
        frame_height = _bsa.read_int()
        print(lbl, "Frame count:", frame_count, "| Width,Height:", frame_width, ",", frame_height)

        # Open up the video writer to write the file
        out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('a', 'v', 'c', '1'), 10, (frame_width, frame_height))
        	# cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
        # While we still have frames to receive
        while frame_count > 0:

            ### Receive frame length ###
            frame_len = _bsa.read_int()

            # if we receive a negative value it means something went wrong
            if frame_len <= 0:
                print(lbl, "Received frame length below 0, ending transaction")
                break

            ### Receive frame data ###
            img = _bsa.read_image(frame_len)
            frame_count -= 1
            # Write the image to our video writer
            out.write(img)

        if frame_count == 0:
            # If we successfully read all the frames we needed to
            ### Receive end of transaction byte ###
            video_res = _bsa.read_int()
            print(lbl, "Done receiving video successfully:", video_res)

        # Release the video writer
        out.release()
        WebAppInterface.getInstance().add_video_data(video_title, received_tags)

    def set_running(self, option: bool):
        self.running = option

    def generate_video_path(self):
        # Replace all the spaces in the name with dashes to avoid upsetting linux
        node_name = self.name.replace(' ', '-')
        # The name of the counter file for this node
        cf_name = "{node_name}.cnt".format(node_name=node_name)
        # the actual path to our counter file
        cf_path = os.path.join(os.getcwd(), 'Videos', 'Counters', cf_name)
        # The video number
        cnt = 0
        # check if the file exists
        if os.path.isfile(cf_path):
            # if the file exists read the int stored in it
            with open(cf_path, 'rb') as file:
                cnt = struct.unpack('i', file.read(4))[0]
            # afterwards overwrite it with the new count
            with open(cf_path, 'wb') as file:
                file.write(struct.pack('i', cnt + 1))
        else:
            with open(cf_path, 'wb') as file:
                file.write(struct.pack("i", 1))

        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        print("date and time:", date_time)
        # The title of the video file
        video_title = "{node_name}-{date_time}-Video-{cnt}.mp4".\
            format(node_name=node_name, date_time=date_time, cnt=cnt)

        video_path = os.path.join(os.getcwd(), 'application', 'static', 'Videos', video_title)
        return video_path, video_title

    def break_down(self):
        print("Breaking down thread: " + self.name)
