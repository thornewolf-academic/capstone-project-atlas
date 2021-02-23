from os import read
from sensor_measurement_parser import BluetoothParser
from utilities import Subscribable,UpdateSignal
import serial
from serial.tools import list_ports
from threading import Thread

class SensorWatcher(Subscribable):
    def __init__(self):
        super(SensorWatcher, self).__init__()
        self.serial = get_arduino_serial()
        self.parser = BluetoothParser()
        self.finished = False
        self.thread = None
    def read_until_complete(self):
        while read_bytes := self.ser.read(1):
            print(read_bytes)
            measurement = self.parser.add_data(read_bytes)
            if measurement is not None:
                self.signal_subscribers(UpdateSignal.NEW_DATA, data=measurement)
    def begin(self):
        t = Thread(target=self.read_until_complete)
        self.thread = t
        self.thread.start()

def get_arduino_serial(baud_rate=9600):
    ports = list_ports.comports()
    arduino_ports = [p for p in ports if 'Arduino' in p.description]
    target_com = arduino_ports[0].device
    return serial.Serial(target_com, baud_rate)


if __name__ == '__main__':
    import time
    watcher = SensorWatcher()
    watcher.begin()
    while not watcher.finished:
        time.sleep(1)
    print('finished sensor watcher test')