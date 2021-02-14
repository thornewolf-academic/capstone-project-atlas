from enum import Enum

class UpdateSignal(Enum):
    NULL = 0
    NEW_DATA = 1
    COMPLETE = 2
    ERROR = 3

class Subscribable:
    def __init__(self):
        self.subscribers = []
    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
    def signal_subscribers(self, signal: UpdateSignal):
        for subscriber in self.subscribers:
            subscriber.signal(signal)

class Subscriber:
    def __init__(self):
        pass
    def signal(self, signal: UpdateSignal):
        return signal