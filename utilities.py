from enum import Enum
import numpy as np


class UpdateSignal(Enum):
    NULL = 0
    NEW_DATA = 1
    COMPLETE = 2
    ERROR = 3


class Subscribable:
    def __init__(self):
        self.subscribers = []
        super().__init__()

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def signal_subscribers(self, signal: UpdateSignal, data=None):
        for subscriber in self.subscribers:
            subscriber.signal(signal, data=data)


class Subscriber:
    def __init__(self):
        super().__init__()

    def signal(self, signal: UpdateSignal, data=None):
        return signal


class SYSTEM_STATES:
    NULL = "NULL"
    LOCALIZE = "LOCALIZE"
    SCAN = "SCAN"
    RESET = "RESET"
    FINISHED = "END SCAN"


def numpy_to_xyz(numpy_path):
    data = np.load(numpy_path)
    data = data[~np.isnan(data[:, 0]), :]
    print(data)
    with open(f"{numpy_path}.xyz", "w") as f:
        for i in range(data.shape[0]):
            s = f"{data[i, 0]} {data[i, 1]} {data[i, 2]}"
            f.write(s + "\n")
