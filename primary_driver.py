import time
import logging
from sensor_watcher import SensorWatcher
from point_cloud_generator import PointCloudGenerator
from real_time_visualizer import RealTimeVisualizer
from data_filterer import DataFilterer
from mesh_generator import MeshGenerator

# Comments are nominal values for Henry's machine
# Updated paths have input, output, and scripts in Project ATLAS directory

POINT_CLOUD_FILE_NAME = '\scan3.xyz'                            #r"\TestMesh.xyz"
POINT_CLOUD_FILE_LOCATION = ATLAS_DIR + '\point_cloud_in'       #r"C:\Users\Henry\PC_Input"
MESH_FILE_NAME = '\mesh3.obj'                                   #r"\OutMesh.obj"
MESH_FILE_LOCATION = ATLAS_DIR + '\mesh_out'                    #r"C:\Users\Henry\PC_Output"
SCRIPT_FILE_NAME = '\script1.mlx'                               #r"\BunnyPoisson.mlx"
SCRIPT_FILE_LOCATION = ATLAS_DIR + '\scripts'                   #r"C:\Users\Henry"


def main():
    logger = logging.Logger("primary_driver", level=logging.INFO)

    sensor_watcher = SensorWatcher()
    point_cloud_generator = PointCloudGenerator(POINT_CLOUD_FILE_NAME)
    real_time_visualizer = RealTimeVisualizer(POINT_CLOUD_FILE_NAME)

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