import time
import logging
import os
import initialize
from mesh_generator import MeshGenerator

def main():
    file_dict = initialize.initialize()
    logger = logging.Logger("primary_driver", level=logging.INFO)

    mesh_generator = MeshGenerator(file_dict)

    mesh_generator.begin()

    while not mesh_generator.finished:
        time.sleep(1)
        logger.info("Completed all ATLAS software :)")

if __name__ == "__main__":
    main()
    