from dataclasses import dataclass
from enum import Enum
from utilities import SYSTEM_STATES


class BluetoothParser:
    def __init__(self):
        self.reset_state()

    def reset_state(self):
        self.data_buffer = ""
        self.state = SYSTEM_STATES.NULL
        self.state_iteration = 0

    def add_data(self, data):
        self.data_buffer += data
        return self.parse_buffer()

    def parse_buffer(self):
        # If we are terminating a message
        message = ""
        if self.data_buffer[-1:] == "\n":
            message = self.data_buffer
            self.data_buffer = ""
        if message == "":
            return
        message_components = message.split(",")

        # See if the received command is to transition into a new state
        if message_components[0] in [SYSTEM_STATES.LOCALIZE, SYSTEM_STATES.SCAN]:
            self.state = message_components[0]
            self.state_iteration = int(message_components[1])
            return
        if message_components[0] in [SYSTEM_STATES.RESET]:
            self.reset_state()
            return

        # Provide message with approprite types and context
        # e.g. ('LOCALIZE', 1, 1, 100, 30, 30)
        return (self.state, self.state_iteration, *map(int, message_components))
