from operator import pos
from utilities import UpdateSignal
from sensor_measurement_parser import BluetoothParser
from point_cloud_generator import PointCloudGenerator
from point_cloud_normalizer import PointCloudNormalizer
import matplotlib.pyplot as plt
import numpy as np

DATA_FILE = "SCAN3.TXT"


def post_process(gen, offset_recommendation=None):
    l1 = gen.my_locations[1]
    l2 = gen.my_locations[2]

    if offset_recommendation is not None:
        l1 = l1 - offset_recommendation[:, :3]

    delta = l2 - l1

    print("my locs", l1, l2)

    # print(np.sqrt(delta[0]))
    print(delta)
    print((delta[0, 0] ** 2 + delta[0, 1] ** 2 + delta[0, 2] ** 2) ** 0.5)


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

    offset_recommendation = None
    if PLOT:
        point_cloud = np.load(DATA_FILE + "_output.npy")
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2])
        plt.show()

    # post_process(gen, offset_recommendation)


if __name__ == "__main__":
    main()