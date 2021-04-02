import time
import logging
import initialize
from sensor_watcher import SensorWatcher
from point_cloud_generator import PointCloudGenerator
from real_time_visualizer import RealTimeVisualizer
from data_filterer import DataFilterer
from mesh_generator import MeshGenerator

def main():
    file_dict = initialize.initialize()
    logger = logging.Logger("primary_driver", level=logging.INFO)

    sensor_watcher = SensorWatcher()
    point_cloud_generator = PointCloudGenerator(file_dict)
    real_time_visualizer = RealTimeVisualizer(file_dict)

    sensor_watcher.add_subscriber(point_cloud_generator)
    point_cloud_generator.add_subscriber(real_time_visualizer)

    sensor_watcher.begin()

    while not sensor_watcher.finished:
        time.sleep(1)

    data_filterer = DataFilterer(file_dict)
    mesh_generator = MeshGenerator(file_dict)

    data_filterer.begin()

    while not data_filterer.finished:
        time.sleep(1)

    mesh_generator.begin()

    while not mesh_generator.finished:
        time.sleep(1)

    logger.info("Completed all ATLAS software :)")


if __name__ == "__main__":
    main()