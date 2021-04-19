import os
import yaml

# Make the folders to store generated files
def make_folders(current_dir, cfg):

    dir_dict = {
        "script_dir": os.path.join(current_dir, cfg["PATHS"]["SCRIPT_LOCATION"]),
        "point_cloud_dir": os.path.join(
            current_dir, cfg["PATHS"]["POINT_CLOUD_LOCATION"]
        ),
        "filt_point_cloud_dir": os.path.join(
            current_dir, cfg["PATHS"]["FILTERED_POINT_CLOUD_LOCATION"]
        ),
        "mesh_dir": os.path.join(current_dir, cfg["PATHS"]["MESH_LOCATION"]),
    }

    for value in dir_dict.values():
        try:
            os.mkdir(value)
        except FileExistsError:
            print("Directory already exists")

    return dir_dict


# Create a file dictionary based on the file names given in config.yaml
def set_files(dir_dict, cfg):
    file_dict = {
        "script_name": os.path.join(
            dir_dict["script_dir"], cfg["NAMES"]["SCRIPT_NAME"]
        ),
        "real_time_point_cloud_name": os.path.join(
            dir_dict["point_cloud_dir"], cfg["NAMES"]["REAL_TIME_POINT_CLOUD_NAME"]
        ),
        "final_point_cloud_name": os.path.join(
            dir_dict["point_cloud_dir"], cfg["NAMES"]["FINAL_POINT_CLOUD_NAME"]
        ),
        "sensor_package_locations_name": os.path.join(
            dir_dict["point_cloud_dir"], cfg["NAMES"]["SENSOR_PACKAGE_LOCATIONS_NAME"]
        ),
        "filt_point_cloud_name": os.path.join(
            dir_dict["filt_point_cloud_dir"], cfg["NAMES"]["FILTERED_POINT_CLOUD_NAME"]
        ),
        "filtered_point_cloud_uncertainty_name": os.path.join(
            dir_dict["filt_point_cloud_dir"], cfg["NAMES"]["UNCERTAINTY_NAME"]
        ),
        "mesh_name": os.path.join(dir_dict["mesh_dir"], cfg["NAMES"]["MESH_NAME"]),
    }

    return file_dict


# Initialization function that contains config loading, parsing, and execution
def initialize():
    current_dir = "."
    config_file = os.path.join(current_dir, "config.yaml")

    with open(config_file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    dir_dict = make_folders(current_dir, cfg)
    file_dict = set_files(dir_dict, cfg)

    return file_dict