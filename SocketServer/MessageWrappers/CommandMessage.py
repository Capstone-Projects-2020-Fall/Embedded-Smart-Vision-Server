from enum import IntEnum


# Enumerator to define the different type of command messages
class CmdTypes(IntEnum):
    # Command for starting and stopping the stream
    STREAM_COMMAND = 0
    TEST_COMMAND = -1


class CommandMessage:
    def __init__(self, command_type):
        self.command_type = command_type


# Command for starting and stopping the stream
class StreamCommand(CommandMessage):
    START_STREAM = 1
    END_STREAM = 2

    def __init__(self, mode):
        super().__init__(CmdTypes.STREAM_COMMAND)
        self.mode = mode


# Test command for testing things
class TestCommand(CommandMessage):
    def __init__(self):
        super().__init__(CmdTypes.TEST_COMMAND)
