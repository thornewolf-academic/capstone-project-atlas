from utilities import Subscriber, Subscribable, UpdateSignal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation, PillowWriter
import time
import threading
from multiprocessing import Process
import uncertainties
from uncertainties import unumpy


class PointCloudVisualizer(Subscriber):
    def __init__(self, file_dict):
        print("Initializing")
        self.point_cloud_file_name = self.file_dict[
            "filtered_point_cloud_uncertainty_name"
        ]
        self.data = np.load(self.point_cloud_file_name, allow_pickle=True)
        print("Loaded data")
        self.fig = plt.figure()

    def begin(self):
        print("Begin")
        self.ax = self.fig.add_subplot(111, projection="3d")

        x = self.data[:, 0]
        print("Read x")
        y = self.data[:, 1]
        print("Read y")
        z = self.data[:, 2]
        print("Read z")

        dx = self.data[:, 3]
        print("Read dx")
        dy = self.data[:, 4]
        print("Read dy")
        dz = self.data[:, 5]
        print("Read dy")

        dtotal = (np.square(dx) + np.square(dy) + np.square(dz)) ** 0.5
        print("Calculated dtotal")

        cm_base = mpl.cm.get_cmap("RdYlGn")
        cm = cm_base.reversed()

        self.scat = self.ax.scatter(x, y, z, c=dtotal, vmin=0, vmax=5, cmap=cm)

        self.minx = min(x)
        self.miny = min(y)
        self.minz = min(z)
        self.maxx = max(x)
        self.maxy = max(y)
        self.maxz = max(z)

        self.ax.set_xlim(self.minx, self.maxx)
        self.ax.set_ylim(self.miny, self.maxy)
        self.ax.set_zlim(self.minz, self.maxz)

        self.ax.set_xlabel("cm")
        self.ax.set_ylabel("cm")
        self.ax.set_zlabel("cm")

        self.ax.xaxis.set_tick_params(labelsize=8)
        self.ax.yaxis.set_tick_params(labelsize=8)
        self.ax.zaxis.set_tick_params(labelsize=8)

        # static axes
        # ax.set_xlim(0, 10)
        # ax.set_ylim(0, 10)
        # ax.set_zlim(0, 10)

        # plt.colorbar(self.scat, label='Uncertainty (cm)', boundaries=np.linspace(0,5,100))
        plt.colorbar(self.scat, label="Uncertainty (cm)")
        self.fig.suptitle("Point Cloud Final")
        plt.show()


if __name__ == "__main__":
    point_cloud_visualizer = PointCloudVisualizer("sample_point_data.npy")
    point_cloud_visualizer.begin()
    print("Done")
