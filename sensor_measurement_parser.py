from dataclasses import dataclass
from enum import Enum
from utilities import SYSTEM_STATES


class BluetoothParser:
    def __init__(self):
        self.reset_state()

    def reset_state(self):
        self.data_buffer = b""
        self.state = SYSTEM_STATES.NULL
        self.state_iteration = 0

    def add_data(self, data):
        self.data_buffer += data
        return self.parse_buffer()

    def interpret_message_components(self, message_components):
        # See if the received command is to transition into a new state
        if message_components[0] in [SYSTEM_STATES.LOCALIZE, SYSTEM_STATES.SCAN]:
            self.state = message_components[0]
            self.state_iteration = int(message_components[1])
            print(f"Got a {message_components[0]} command")
            return
        if message_components[0] in [SYSTEM_STATES.RESET]:
            self.reset_state()
            return

        # Provide message with approprite types and context
        # e.g. ('LOCALIZE', 1, 1, 100, 30, 30)
        return (
            self.state,
            self.state_iteration,
            *map(clean_parse_float, message_components),
        )

    def parse_buffer(self):
        # If we are terminating a message
        buffer = self.data_buffer
        buffer_as_string = "".join(map(chr, list(buffer)))

        # We dump the startup bluetooth serial message
        if "BTserial" in buffer_as_string and "\r\n" in buffer_as_string:
            self.data_buffer = b""
            return

        message = ""
        if buffer_as_string[-1:] == "\n":
            message = buffer_as_string
            print(message)
            self.data_buffer = b""
        if message == "":
            return

        message_components = message.split(",")
        interpretation = None
        try:
            interpretation = self.interpret_message_components(message_components)
        except Exception as e:
            print(e)
            pass
        return interpretation


def clean_parse_float(val):
    val = val.replace("\n", "")
    val = val.replace("\r", "")
    return float(val)
