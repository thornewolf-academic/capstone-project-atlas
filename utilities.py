from enum import Enum

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
    NULL = 'NULL'
    LOCALIZE = 'LOCALIZE'
    SCAN = 'SCAN'
    RESET = 'RESET'