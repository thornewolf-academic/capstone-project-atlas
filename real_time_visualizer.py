from utilities import Subscriber, Subscribable, UpdateSignal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation, PillowWriter
import time
import threading
from multiprocessing import Process


class RealTimeVisualizer(Subscriber):
    def __init__(self, point_cloud_file_name):
        intvl = 1000  # ms
        self.point_cloud_file_name = point_cloud_file_name
        self.data = np.array([[], [], []])
        self.minx = 0
        self.miny = 0
        self.minz = 0
        self.maxx = 0
        self.maxy = 0
        self.maxz = 0
        self.initial_time = time.time()
        self.last_time = time.time()
        self.current_time = time.time()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.scat = self.ax.scatter([], [], [])

        self.num_rows = 0

        p = Process(target=self.myplot, args=(intvl,))
        p.start()

    def myplot(self, intvl):
        self.ani = animation.FuncAnimation(
            self.fig, self.update_plot, blit=False, interval=intvl, repeat=False
        )
        plt.show()

    def update_plot(self, i):
        try:
            self.data = np.load(f"{self.point_cloud_file_name}.npy", allow_pickle=True)
        except Exception as e:
            print("could not read file")
            print(e)
            return

        if self.data.shape[0] != self.num_rows:
            try:
                x = self.data[:, 0]
                y = self.data[:, 1]
                z = self.data[:, 2]
                self.minx = max(min(self.minx, min(x[self.num_rows :])), -2000)
                self.miny = max(min(self.miny, min(y[self.num_rows :])), -2000)
                self.minz = max(min(self.minz, min(z[self.num_rows :])), -2000)
                self.maxx = min(max(self.maxx, max(x[self.num_rows :])), 2000)
                self.maxy = min(max(self.maxy, max(y[self.num_rows :])), 2000)
                self.maxz = min(max(self.maxz, max(z[self.num_rows :])), 2000)
            except Exception as e:
                print(e)
                return

            self.num_rows = self.data.shape[0]

        x = self.data[:, 0]
        y = self.data[:, 1]
        z = self.data[:, 2]

        self.current_time = time.time()
        self.elapsed_time = "%.2f" % (self.current_time - self.initial_time)
        self.last_time = self.current_time

        self.ax.set_xlim(self.minx, self.maxx)
        self.ax.set_ylim(self.miny, self.maxy)
        self.ax.set_zlim(self.minz, self.maxz)

        # static axes
        # ax.set_xlim(0, 10)
        # ax.set_ylim(0, 10)
        # ax.set_zlim(0, 10)

        self.scat._offsets3d = (x, y, z)
        numpoints = "Number of Points: " + str(self.num_rows)
        time_elapsed = "Time Elapsed: " + str(self.elapsed_time) + "s  "
        iteration = " Iteration: " + str(i)
        self.fig.suptitle(time_elapsed + numpoints + iteration)

        # needs update to use animation
        # f = r"C:\Users\victo\OneDrive\Desktop\2020-2021\SPR21\AE445 Detail\real_time.gif"
        # writergif = animation.PillowWriter(fps=10)
        # ani.save(f, writer=writergif)

    def signal(self, signal: UpdateSignal, data=None):
        try:
            self.data = np.load(self.point_cloud_file_name, allow_pickle=True)
        except:
            return

        if self.data.shape[0] != self.num_rows:
            try:
                x = self.data[:, 0]
                y = self.data[:, 1]
                z = self.data[:, 2]
                self.minx = min(self.minx, min(x[self.num_rows :]))
                self.miny = min(self.miny, min(y[self.num_rows :]))
                self.minz = min(self.minz, min(z[self.num_rows :]))
                self.maxx = max(self.maxx, max(x[self.num_rows :]))
                self.maxy = max(self.maxy, max(y[self.num_rows :]))
                self.maxz = max(self.maxz, max(z[self.num_rows :]))
            except Exception as e:
                print(e)
                return

            self.num_rows = self.data.shape[0]

        return signal


if __name__ == "__main__":
    RealTimeVisualizer("sample_point_data.npy")
