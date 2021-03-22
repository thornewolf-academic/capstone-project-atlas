import time
import logging
import os
from mesh_generator import MeshGenerator

ATLAS_DIR = os.path.dirname(__file__)

POINT_CLOUD_FILE_NAME = '\scan_test.xyz'                        #r"\TestMesh.xyz"
POINT_CLOUD_FILE_LOCATION = ATLAS_DIR + '\point_cloud_in'       #r"C:\Users\Henry\PC_Input"
MESH_FILE_NAME = '\mesh_test.obj'                               #r"\OutMesh.obj"
MESH_FILE_LOCATION = ATLAS_DIR + '\mesh_out'                    #r"C:\Users\Henry\PC_Output"
SCRIPT_FILE_NAME = '\script1.mlx'                               #r"\BunnyPoisson.mlx"
SCRIPT_FILE_LOCATION = ATLAS_DIR + '\scripts'                   #r"C:\Users\Henry"

def main():
    logger = logging.Logger("primary_driver", level=logging.INFO)

    mesh_generator = MeshGenerator(POINT_CLOUD_FILE_NAME, POINT_CLOUD_FILE_LOCATION, MESH_FILE_NAME, MESH_FILE_LOCATION, SCRIPT_FILE_NAME, SCRIPT_FILE_LOCATION)

    mesh_generator.begin()

    while not mesh_generator.finished:
        time.sleep(1)
        logger.info("Completed all ATLAS software :)")

if __name__ == "__main__":
    main()
    