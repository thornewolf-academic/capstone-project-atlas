from primary_driver import POINT_CLOUD_FILE_NAME
import time
from real_time_visualizer import RealTimeVisualizer
import logging
from utilities import UpdateSignal
from sensor_measurement_parser import BluetoothParser
from point_cloud_generator import PointCloudGenerator
from point_cloud_normalizer import PointCloudNormalizer
from mesh_generator import MeshGenerator
from data_filterer import DataFilterer
from point_cloud_visualizer import PointCloudVisualizer
import matplotlib.pyplot as plt
import numpy as np

RAW_DATA_PATH = "abridged_point_scan.TXT"
POINT_CLOUD_FILE_NAME = RAW_DATA_PATH + ".npy"
FILTERED_DATA_PATH = "filtered_point_cloud.npy"
UNCERTAINTY_PATH = "uncertainty_output.npy"
MESH_PATH = "final_mesh.obj"
SCRIPT_PATH = "./scripts/script1.mlx"

PLOT = True


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

    # We need to fake out the data passed to PointCloudGenerator. This process does so.
    parser = BluetoothParser()
    gen = PointCloudGenerator(POINT_CLOUD_FILE_NAME)
    real_time_visualizer = RealTimeVisualizer(POINT_CLOUD_FILE_NAME)

    # The parser expects byte data like the serial passes.
    with open(RAW_DATA_PATH, "rb") as f:
        data = f.read()

    for c in data:
        r = parser.add_data(bytes((c,)))
        if r is not None:
            gen.signal(UpdateSignal.NEW_DATA, r)

    gen.mark_finished()
    # time.sleep(5)

    data_filterer = DataFilterer(
        POINT_CLOUD_FILE_NAME, FILTERED_DATA_PATH, UNCERTAINTY_PATH
    )
    mesh_generator = MeshGenerator(
        FILTERED_DATA_PATH + ".xyz", ".\\", MESH_PATH, ".\\", SCRIPT_PATH, ".\\"
    )

    data_filterer.begin()

    while not data_filterer.finished:
        time.sleep(1)

    numpy_to_xyz(FILTERED_DATA_PATH)

    mesh_generator.begin()

    while not mesh_generator.finished:
        time.sleep(1)

    point_cloud_visualizer = PointCloudVisualizer(FILTERED_DATA_PATH)
    point_cloud_visualizer.begin()

    logger.info("Completed all ATLAS software :)")


if __name__ == "__main__":
    main()