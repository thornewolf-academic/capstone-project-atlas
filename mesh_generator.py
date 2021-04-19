import os
import logging
import subprocess

# Holds all file location and file names as properties of the class. All functions for automated meshing are contained within the class.
class MeshGenerator:
    def __init__(self, file_dict):
        self.finished = 0
        self.file_dict = file_dict

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)

    # Create the strings for the automatic meshing that will run in the command line.
    def generate_commands(self):

        meshserver_dir = (
            "C:\Program Files\VCG\MeshLab\meshlabserver.exe"  # Default install location
        )
        # meshserver_dir = clean_string_for_windows(meshserver_dir)

        in_f = self.file_dict["filt_point_cloud_name"]
        out_f = self.file_dict["mesh_name"]
        script_f = self.file_dict["script_name"]

        command_mesh = f'"{meshserver_dir}" -i "{in_f}" -o "{out_f}" -s "{script_f}"'
        self.logger.info(f"{command_mesh=}")

        command_launch = f"start MeshLab {out_f}"

        return {"mesh": command_mesh, "launch": command_launch}

    # Run the generated strings in the command line.
    def auto_mesh(self):
        # It might be better to add the input and output directories as ENV_VARS or auto-generate them.
        os.system("echo Running Mesh Step... ")

        # IMPORTANT: Default input args for Henry's machine: r"\TestMesh.xyz", r"C:\Users\Henry\PC_Input", r"\OutMesh.obj", r"C:\Users\Henry\PC_Output", r"\BunnyPoisson.mlx", r"C:\Users\Henry"
        command_dict = self.generate_commands()

        subprocess.call(command_dict["mesh"])
        os.system(command_dict["launch"])

        os.system("echo Complete, Opening Mesh... ")

    # Begin the automatic meshing process.
    def begin(self):
        self.auto_mesh()
        self.finished = 1
