import struct
import SocketServer.MessageDataParser as mdp
from SocketServer.MessagePack import MessagePack, MsgType, build_from_bytes
from SocketServer.MessageWrappers.CommandMessage import StreamCommand, TestCommand


# Helper function inplace of unit testing functions
def test_true(exp, act, message, func):
    if exp != act:
        print("\nFailed test in function:", func)
        print(message)
        print("Expected {exp} , but got {act}\n".format(exp=exp, act=act))
        return False
    return True


# This file is not needed for functionality but acts as a place to add functions to test various key features
# Quick test to ensure stripping bytes isn't doing anything weird
def test_strip_bytes():
    result = True

    print("testing the stripping of bytes\n")
    test_array = struct.pack('iii', 1, 2, 3)
    print("Starting bytes:", test_array)

    result = test_true(12, len(test_array), "Byte arrays where not the right length!", "TestFile.test_strip_bytes")

    # test we stripped the first bytes properly
    first_number_bytes, test_array = mdp.strip_bytes(4, test_array)
    first_number = struct.unpack('i', first_number_bytes)[0]
    print()
    print("Stripped bytes:", first_number_bytes)
    print("Remaining bytes:", test_array)

    result = test_true(8, len(test_array), "Byte arrays where not the right length!", "TestFile.test_strip_bytes")

    # test we stripped the second bytes properly
    second_number_bytes, test_array = mdp.strip_bytes(4, test_array)
    second_number = struct.unpack('i', second_number_bytes)[0]
    print()
    print("Stripped bytes:", second_number_bytes)
    print("Remaining bytes:", test_array)
    result = test_true(4, len(test_array), "Byte arrays where not the right length!", "TestFile.test_strip_bytes")

    # Test we stripped the final bytes properly
    third_number_bytes, test_array = mdp.strip_bytes(4, test_array)
    third_number = struct.unpack('i', third_number_bytes)[0]
    print()
    print("Stripped bytes:", third_number_bytes)
    print("Remaining bytes:", test_array)
    result = test_true(0, len(test_array), "Byte arrays where not the right length!", "TestFile.test_strip_bytes")

    print("\nRetrieved Number ({one}, {two}, {tre})".format(one=first_number,
                                                            two=second_number,
                                                            tre=third_number))


# Quick test to make sure the function is bounded to avoid crashing
def test_strip_bytes_bounding():
    print("testing the stripping of bytes\n")
    test_array = struct.pack('iii', 1, 2, 3)
    print("Starting bytes:", test_array)

    print("\nTest stripping 0 bytes")
    tmp, test_array = mdp.strip_bytes(0, test_array)
    print("Stripped bytes:", tmp)
    print("Remaining bytes:", test_array)
    print("Stripped length:", len(tmp))
    print("Remaining length:", len(test_array))

    print("\nTest stripping negative bytes")
    tmp, test_array = mdp.strip_bytes(-542, test_array)
    print("Stripped bytes:", tmp)
    print("Remaining bytes:", test_array)
    print("Stripped length:", len(tmp))
    print("Remaining length:", len(test_array))

    print("\nTest stripping more then 12 bytes")
    tmp, test_array = mdp.strip_bytes(15, test_array)
    print("Stripped bytes:", tmp)
    print("Remaining bytes:", test_array)
    print("Stripped length:", len(tmp))
    print("Remaining length:", len(test_array))

    print("\nTest stripping exactly 12 bytes")
    tmp, test_array = mdp.strip_bytes(12, test_array)
    print("Stripped bytes:", tmp)
    print("Remaining bytes:", test_array)
    print("Stripped length:", len(tmp))
    print("Remaining length:", len(test_array))


def test_create_stream_command():
    stream_command = StreamCommand(StreamCommand.START_STREAM)

    print("Command Type:", stream_command.command_type)
    print("Stream Mode:", stream_command.mode)


def test_encode_decode_stream_command():
    stream_command = StreamCommand(StreamCommand.START_STREAM)
    stream_bytes = mdp.stream_command_to_bytes(stream_command)
    print("Original Command Type:", stream_command.command_type)
    print("Original Stream Mode:", stream_command.mode)

    decoded_stream_command: StreamCommand = mdp.bytes_to_command(stream_bytes)
    print("Command Type:", decoded_stream_command.command_type)
    print("Stream Mode:", decoded_stream_command.mode)

    test_true(stream_command.command_type,
              decoded_stream_command.command_type,
              "Expected to have the same command type",
              "test_encode_decode_stream_command")

    test_true(stream_command.mode,
              decoded_stream_command.mode,
              "Expected to have the same mode",
              "test_encode_decode_stream_command")


# Test that we can properly encode and decode the message packs
def test_encode_decode_message_pack():
    msg_pack = MessagePack(message_type=MsgType.COMMAND)
    str_cmd = StreamCommand(StreamCommand.START_STREAM)
    msg_pack.set_data(str_cmd)
    msg_pack.print_package()
    msg_bytes = msg_pack.create_byte_array()
    print(msg_bytes)
    print("\n")

    # Pretend to read the header like in the actual stream by stripping bytes
    received_bytes, msg_bytes = mdp.strip_bytes(8, msg_bytes)
    data_length, msg_type = struct.unpack('ii', received_bytes)

    decoded_msg_pack = build_from_bytes(msg_type, data_length, msg_bytes)
    decoded_msg_pack.print_package()
    decoded_stream_package: StreamCommand = decoded_msg_pack.data
    print("Decoded command type:", decoded_stream_package.command_type)
    print("Decoded Stream mode:", decoded_stream_package.mode)

def test_size_inherits_properly():
    str_cmd = StreamCommand(StreamCommand.START_STREAM)
    print(str_cmd.size)

    tst_cmd = TestCommand()
    print(tst_cmd.size)


test_encode_decode_message_pack()
# test_encode_decode_stream_command()
# test_strip_bytes_bounding()
# raw_data = struct.pack('iii', 1, 2, 3)
# mdp.bytes_to_command(raw_data)
