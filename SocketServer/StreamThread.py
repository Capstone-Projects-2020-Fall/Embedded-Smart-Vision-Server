# This thread will be spawned and started when a node connects in stream mode
# This class handles all the outgoing traffic and messages
import threading


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
            print("STRREEEEAAAMMMING")

