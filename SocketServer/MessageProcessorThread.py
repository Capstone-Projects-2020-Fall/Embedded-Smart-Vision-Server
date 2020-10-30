# This class handles all the outgoing traffic and messages
import threading
from queue import Queue

from SocketServer.MessagePack import MessagePack, MsgType
from SocketServer.MessageWrappers.CommandMessage import CommandMessage, CmdTypes
from SocketServer.QueueMessage import QueueMessage


def handle_stream_command(node_origin, cmd: CommandMessage):
    print("Starting stream for node {node_name}".format(node_name=node_origin))


def handle_command_message(node_origin, cmd: CommandMessage):
    print("HANDLING COMMAND MESSAGE")
    if cmd.command_type == CmdTypes.STREAM_COMMAND:
        # Handle a stream command
        handle_stream_command(node_origin, cmd)


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
            print("New message from the queue!")

            msg_pack: MessagePack = msg.msg_package

            if msg_pack.header.messageType == MsgType.COMMAND:
                handle_command_message(msg.node_origin, msg_pack.data)
