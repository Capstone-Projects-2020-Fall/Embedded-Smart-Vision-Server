# This class handles all the outgoing traffic and messages
import threading


class OutgoingThread(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.ThreadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting" + self.name)
