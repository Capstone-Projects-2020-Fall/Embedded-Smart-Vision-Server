import pickle
import struct
from socket import socket


# A class that takes in a socket connection and treats it like a byte stream for peeling data
class bs_adapter:
    SRL_PICKLED = 1

    def __init__(self, conn: socket):
        self.conn = conn

    # Helper function to read and reconstruct bytes that may have been coalesced by the socket
    def get_bytes(self, cnt: int):
        buf_size = 4096
        remaining_bytes = cnt
        data = bytearray()
        while True:
            if remaining_bytes < buf_size:
                # If we have less bytes remaining
                # to receive then the buffer size receive only those bytes
                tmp = self.conn.recv(remaining_bytes)
                data.extend(tmp)
                break
            else:
                # If we are still taking full buffers take full buffers
                data += self.conn.recv(buf_size)
                # Keep track of how many bytes we have consumed
                remaining_bytes = remaining_bytes - buf_size
        return data

    def read_int(self):
        # Read off the top 4 bytes
        b_arr = self.get_bytes(4)
        # Unpack the integer and return it
        return struct.unpack('i', b_arr)[0]

    def read_string(self, cnt):
        b_arr = self.get_bytes(cnt)
        # Decode and return the string
        return b_arr.decode('utf-8')

    def read_image(self, cnt, serializer=SRL_PICKLED):
        b_arr = self.get_bytes(cnt)
        img = None
        if serializer == self.SRL_PICKLED:
            img = pickle.loads(b_arr)

        return img
