from utilities import Subscribable

class SensorWatcher(Subscribable):
    def __init__(self):
        super(SensorWatcher, self).__init__()
        self.finished = False
    def begin(self):
        pass
