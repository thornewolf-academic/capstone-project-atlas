import time
import logging
from sensor_watcher import SensorWatcher
from point_cloud_generator import PointCloudGenerator
from real_time_visualizer import RealTimeVisualizer
from data_filterer import DataFilterer
from mesh_generator import MeshGenerator

SENSOR_DATA_FILE_NAME = ''
POINT_CLOUD_FILE_NAME = ''
FILTERED_POINT_CLOUD_FILE_NAME = ''
MESH_FILE_NAME = ''

def main():
    logger = logging.Logger('primary_driver', level=logging.INFO)

    sensor_watcher = SensorWatcher()
    point_cloud_generator = PointCloudGenerator(SENSOR_DATA_FILE_NAME, POINT_CLOUD_FILE_NAME)
    real_time_visualizer = RealTimeVisualizer()

    sensor_watcher.add_subscriber(point_cloud_generator)
    point_cloud_generator.add_subscriber(real_time_visualizer)
    
    sensor_watcher.begin()

    while not sensor_watcher.finished:
        time.sleep(1)

    data_filterer = DataFilterer()
    mesh_generator = MeshGenerator()

    data_filterer.begin()

    while not data_filterer.finished:
        time.sleep(1)
    
    mesh_generator.begin()

    while not mesh_generator.finished:
        time.sleep(1)

    logger.info("Completed all ATLAS software :)")