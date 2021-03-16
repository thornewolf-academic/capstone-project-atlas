import os

# Holds all file location and file names as properties of the class. All functions for automated meshing are contained within the class.
class MeshGenerator:

    def __init__(self, in_file, in_dir, out_file, out_dir, script_file, script_dir):
        self.finished = 0    
        self.in_file = in_file 
        self.in_dir = in_dir 
        self.out_file = out_file 
        self.out_dir = out_dir 
        self.script_file = script_file 
        self.script_dir = script_dir   

    # Create the strings for the automatic meshing that will run in the command line.
    def generate_commands(self):

        meshserver_dir = "C:\Program Files\VCG\MeshLab\meshlabserver.exe" # Default install location
        meshserver_dir_f = f'"{meshserver_dir}"'

        in_f = f"{self.in_dir}{self.in_file}"
        out_f = f"{self.out_dir}{self.out_file}"
        script_f = f"{self.script_dir}{self.script_file}"

        command_init = f"{meshserver_dir_f}"

        command_mesh = f"{meshserver_dir_f} -i {in_f} -o {out_f} -s {script_f}"

        command_launch = f"start MeshLab {out_f}"

        return {'init': command_init, 'mesh': command_mesh, 'launch': command_launch}

    # Run the generated strings in the command line.
    def auto_mesh(self):
        # It might be better to add the input and output directories as ENV_VARS or auto-generate them.
        os.system("echo Running... ")

        # IMPORTANT: Default input args for Henry's machine: r"\TestMesh.xyz", r"C:\Users\Henry\PC_Input", r"\OutMesh.obj", r"C:\Users\Henry\PC_Output", r"\BunnyPoisson.mlx", r"C:\Users\Henry"
        command_dict = self.generate_commands()

        #print(command_dict['init'])
        print(command_dict['mesh'])
        print(command_dict['launch'])

        #os.system(command_dict['init'])
        os.system(command_dict['mesh'])
        os.system(command_dict['launch'])

        os.system("echo Complete")

    # Begin the automatic meshing process.
    def begin(self):
            self.auto_mesh()
            self.finished = 1





