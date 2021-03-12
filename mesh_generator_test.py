import time
import logging
from mesh_generator import MeshGenerator

POINT_CLOUD_FILE_NAME = r"\TestMesh.xyz"
POINT_CLOUD_FILE_LOCATION = r"C:\Users\Henry\PC_Input"
MESH_FILE_NAME = r"\OutMesh.obj"
MESH_FILE_LOCATION = r"C:\Users\Henry\PC_Output"
SCRIPT_FILE_NAME = r"\BunnyPoisson.mlx"
SCRIPT_FILE_LOCATION = r"C:\Users\Henry"


def main():
    logger = logging.Logger("primary_driver", level=logging.INFO)

    mesh_generator = MeshGenerator(POINT_CLOUD_FILE_NAME, POINT_CLOUD_FILE_LOCATION, MESH_FILE_NAME, MESH_FILE_LOCATION, SCRIPT_FILE_NAME, SCRIPT_FILE_LOCATION)

    mesh_generator.begin()

    while not mesh_generator.finished:
        time.sleep(1)
        logger.info("Completed all ATLAS software :)")

if __name__ == "__main__":
    main()
    