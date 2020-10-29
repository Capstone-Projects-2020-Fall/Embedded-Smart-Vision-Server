# This class handles all the outgoing traffic and messages
import threading
from queue import Queue

from SocketServer.QueueMessage import QueueMessage


class MessageProcessorThread(threading.Thread):

    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.message_queue: Queue = message_queue
        self.running = True
        self.name = "Message Processor Thread"

    def run(self):
        print("Starting" + self.name)
        while self.running:
            msg: QueueMessage = self.message_queue.get()
            msg.print_message_content()
