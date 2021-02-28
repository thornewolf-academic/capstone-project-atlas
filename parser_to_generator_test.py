from utilities import UpdateSignal
from sensor_measurement_parser import BluetoothParser
from point_cloud_generator import PointCloudGenerator

DATA_FILE = "SCAN3.TXT"


def main():
    parser = BluetoothParser()
    gen = PointCloudGenerator(DATA_FILE + "_output")
    with open(DATA_FILE, "r") as f:
        data = f.read()
    for i, c in enumerate(data):
        r = parser.add_data(c)
        if r is not None:
            gen.signal(UpdateSignal.NEW_DATA, r)
            # print(r)
    l1 = gen.my_locations[1]
    l2 = gen.my_locations[2]
    delta = l2 - l1
    import numpy as np
    import math

    # print(np.sqrt(delta[0]))
    print(delta)
    print((delta[0, 0] ** 2 + delta[0, 1] ** 2 + delta[0, 2] ** 2) ** 0.5)


if __name__ == "__main__":
    main()