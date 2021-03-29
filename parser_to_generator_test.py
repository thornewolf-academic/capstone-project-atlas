from operator import pos
from utilities import UpdateSignal
from sensor_measurement_parser import BluetoothParser
from point_cloud_generator import PointCloudGenerator
import matplotlib.pyplot as plt
import numpy as np

DATA_FILE = "testing_data_files/SCAN_FAKE.TXT"


PLOT = True


def main():
    parser = BluetoothParser()
    gen = PointCloudGenerator(DATA_FILE + "_output")
    with open(DATA_FILE, "rb") as f:
        data = f.read()

    for i, c in enumerate(data):
        r = parser.add_data(bytes((c,)))
        if r is not None:
            gen.signal(UpdateSignal.NEW_DATA, r)
    gen.mark_finished()

    if PLOT:
        point_cloud = np.load(DATA_FILE + "_output.npy")
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2])
        plt.show()


if __name__ == "__main__":
    main()