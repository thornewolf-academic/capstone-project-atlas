import time
from real_time_visualizer import RealTimeVisualizer
import logging
from utilities import UpdateSignal
from sensor_measurement_parser import BluetoothParser
from point_cloud_generator import PointCloudGenerator
from mesh_generator import MeshGenerator
from data_filterer import DataFilterer
from point_cloud_visualizer import PointCloudVisualizer
import matplotlib.pyplot as plt
import numpy as np
import initialize

RAW_DATA_PATH = "2_point_scan_4.5.TXT"
POINT_CLOUD_FILE_NAME = RAW_DATA_PATH + ".npy"
PACKAGE_LOCATIONS_FILE_NAME = "sensor_package_locations.npy"
FILTERED_DATA_PATH = "filtered_point_cloud.npy"
UNCERTAINTY_PATH = "uncertainty_output.npy"
MESH_PATH = "final_mesh.obj"
SCRIPT_PATH = "./scripts/script1.mlx"

PLOT = True

logging.basicConfig(filename="runs.log", level=logging.INFO)


def numpy_to_xyz(numpy_path):
    data = np.load(numpy_path)
    data = data[~np.isnan(data[:, 0]), :]
    print(data)
    with open(f"{numpy_path}.xyz", "w") as f:
        for i in range(data.shape[0]):
            s = f"{data[i, 0]} {data[i, 1]} {data[i, 2]}"
            f.write(s + "\n")


def main():
    logger = logging.Logger("pipeline_test", level=logging.INFO)

    configuration_dictionary = initialize.initialize()

    # We need to fake out the data passed to PointCloudGenerator. This process does so.
    parser = BluetoothParser()
    gen = PointCloudGenerator(configuration_dictionary)
    real_time_visualizer = RealTimeVisualizer(configuration_dictionary)

    # The parser expects byte data like the serial passes.
    with open(RAW_DATA_PATH, "rb") as f:
        data = f.read()

    for c in data:
        r = parser.add_data(bytes((c,)))
        if r is not None:
            gen.signal(UpdateSignal.NEW_DATA, r)

    gen.mark_finished()

    data_filterer = DataFilterer(configuration_dictionary)

    data_filterer.begin()

    while not data_filterer.finished:
        time.sleep(1)

    mesh_generator = MeshGenerator(configuration_dictionary)
    mesh_generator.begin()

    while not mesh_generator.finished:
        time.sleep(1)

    point_cloud_visualizer = PointCloudVisualizer(configuration_dictionary)
    point_cloud_visualizer.begin()

    logger.info("Completed all ATLAS software :)")


if __name__ == "__main__":
    main()