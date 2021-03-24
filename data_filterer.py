import numpy as np
from uncertainties import unumpy as unp
from uncertainties import umath
import numpy as np
import matplotlib.pyplot as plt 
import csv
from mpl_toolkits.mplot3d import Axes3D
import scipy.integrate as integrate
import scipy.special as special
import FWOCFM 
import TDLS
import winsound

class DataFilterer:
    def __init__(self,data_in_path,filt_point_cloud_path,uncertainty_path):
        #self.data_in_path = data_in_path
        self.finished = 0
        self.data = np.load(data_in_path)
        self.filt_point_cloud_path = filt_point_cloud_path
        self.uncertainty_path = uncertainty_path

    def begin(self):
        self.filt_data = self.filtering()
        np.save(self.filt_point_cloud_path,self.filt_data)
        self.error = self.uncertainty()
        np.save(self.uncertainty_path,self.error)

    def filtering(self):
        rows = []
        for row in self.data:
            rows.append(row)
        X = [float(row[0]) for row in rows]
        Y = [float(row[1]) for row in rows]
        Z = [float(row[2]) for row in rows]
        X_n = np.array(X)
        Y_n = np.array(Y)
        Z_n = np.array(Z)

        first_pass_data = FWOCFM.FWOCFM(Z_n)

        second_pass_data = TDLS.TDLS(X_n,Y_n,first_pass_data)

        filt_data = [X, Y, second_pass_data]

        winsound.Beep(1000, 750)
        print('DATA FILTER COMPLETE')

        return filt_data

    def uncertainty(self):
        rows = []
        for row in self.data:
            rows.append(row)
        X = [float(row[0]) for row in rows]
        Y = [float(row[1]) for row in rows]
        Z = [float(row[2]) for row in rows]
        X_n = np.array(X)
        Y_n = np.array(Y)
        Z_n = np.array(Z)

        u_x = std_devs(X_n)
        u_y = std_devs(Y_n)
        u_z = np.abs(filt_data[:,3]-Z_n + std.devs(Z_n))
        uncertainty = np.append(u_x,u_y)
        uncertainty = np.append(uncertainty,u_z)

        return uncertainty

