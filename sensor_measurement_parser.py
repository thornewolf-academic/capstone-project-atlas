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

    def validate_message_components(self, message_components):
        """
        We need to ensure that a received message on matches predefined allowed formats.
        LOCALIZE,#
        #,#,#,#
        SCAN,#
        #,#,#
        """

        # Localization validation
        if (
            len(message_components) == 2
            and message_components[0] == "LOCALIZE"
            and message_components[1].isnumeric()
        ):
            return True
        # Scan validation
        if (
            len(message_components) == 2
            and message_components[0] == "SCAN"
            and message_components[1].isnumeric()
        ):
            return True
        # Localization data validation
        if len(message_components) == 4 and all(
            comp.replace("-", "").isnumeric() for comp in message_components
        ):
            return True
        # Scan data validation
        if len(message_components) == 3 and all(
            comp.isnumeric() for comp in message_components
        ):
            return True
        # Finished command
        if (
            len(message_components) == 1
            and message_components[0] == SYSTEM_STATES.FINISHED
        ):
            return True
        return False

    def interpret_message_components(self, message_components):
        if not self.validate_message_components(message_components):
            print(f"Received garbage data on parser")
            print(f"{message_components=}")
            return

        # See if the received command is to transition into a new state
        if message_components[0] in [SYSTEM_STATES.LOCALIZE, SYSTEM_STATES.SCAN]:
            self.state = message_components[0]
            self.state_iteration = int(message_components[1])
            if message_components[0] == SYSTEM_STATES.LOCALIZE:
                print(f"Got a {message_components[0]} command, {message_components[1]}")
            return
        if message_components[0] in [SYSTEM_STATES.RESET]:
            self.reset_state()
            return

        if message_components[0] in [SYSTEM_STATES.FINISHED]:
            self.state = SYSTEM_STATES.FINISHED
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
        message_components = [comp.strip() for comp in message_components]
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
