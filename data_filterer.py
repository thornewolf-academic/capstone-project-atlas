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
import matcher
import winsound
import progressbar
from time import sleep
import time

start = time.time()

class DataFilterer:
    def __init__(self,file_dict):
        #self.data_in_path = data_in_path
        self.finished = 0
        self.file_dict = file_dict 
        self.data = np.load(self.file_dict["point_cloud_name"])
        self.filt_point_cloud_path = file_dict["filtered_point_cloud_name"]
        self.uncertainty_path = self.file_dict["filtered_point_cloud_uncertainty_name"]

    def begin(self):
        self.fixed_data = self.surface_match()
        self.filt_data = self.filtering()
        np.savetxt(self.filt_point_cloud_path,self.filt_data,delimiter=' ')
        self.error = self.uncertainty()
        self.error = np.hstack((self.filt_data, self.error))
        np.save(self.uncertainty_path,self.error)

        end = time.time()
        print('DATA PROCESSSING TIME:', (end - start),'S')
    
    def surface_match(self):
        data = self.data
        L = np.asarray(data[:,0])
        dataset1 = np.zeros([len(L),4])
        dataset2 = np.zeros([len(L),4])
        dataset3 = np.zeros([len(L),4])
        dataset4 = np.zeros([len(L),4])
        dataset5 = np.zeros([len(L),4])
        dataset6 = np.zeros([len(L),4])
        dataset7 = np.zeros([len(L),4])
        dataset8 = np.zeros([len(L),4])
        dataset9 = np.zeros([len(L),4])
        datasetmisc = np.zeros([len(L),4])
        locations = np.max(L)
        print('NUMBER OF LOCATIONS:', int(locations))
        for loc in range(0,len(data)):
            if 1 == data[loc,0]:
                dataset1[loc,:] = data[loc,0:4]
            elif 2 == data[loc,0]:
                dataset2[loc,:] = data[loc,0:4]
            elif 3 == data[loc,0]:
                dataset3[loc,:] = data[loc,0:4]
            elif 4 == data[loc,0]:
                dataset4[loc,:] = data[loc,0:4]
            elif 5 == data[loc,0]:
                dataset5[loc,:] = data[loc,0:4]
            elif 6 == data[loc,0]:
                dataset6[loc,:] = data[loc,0:4]
            elif 7 == data[loc,0]:
                dataset7[loc,:] = data[loc,0:3]
            elif 8 == data[loc,0]:
                dataset8[loc,:] = data[loc,0:3]
            elif 9 == data[loc,0]:
                dataset9[loc,:] = data[loc,0:3]
            else:
                datasetmisc = data[loc,0:3]

        for loc in range(1,int(locations)+1):
            if loc == 1:
                dataset1 =  dataset1[~np.all(dataset1 == 0, axis=1)]
            elif loc == 2:
                dataset2 =  dataset2[~np.all(dataset2 == 0, axis=1)]
                dataset2_fixed = matcher.surface_match(dataset1,dataset2)
                dataset1_new = np.vstack((dataset1,dataset2_fixed))
            elif loc == 3:
                dataset3 =  dataset3[~np.all(dataset3 == 0, axis=1)]
                dataset3_fixed = matcher.surface_match(dataset1_new,dataset3)
                dataset1_new = np.vstack((dataset1_new,dataset3_fixed))
            elif loc == 4:
                dataset4 =  dataset4[~np.all(dataset4 == 0, axis=1)]
                dataset4_fixed = matcher.surface_match(dataset1_new,dataset4)
                dataset1_new = np.vstack((dataset1_new,dataset4_fixed))
            elif loc == 5:
                dataset5 =  dataset5[~np.all(dataset5 == 0, axis=1)]
                dataset5_fixed = matcher.surface_match(dataset1_new,dataset5)
                dataset1_new = np.vstack((dataset1_new,dataset5_fixed))
            elif loc == 6:
                dataset6 =  dataset6[~np.all(dataset6 == 0, axis=1)]
                dataset6_fixed = matcher.surface_match(dataset6_new,dataset6)
                dataset1_new = np.vstack((dataset1_new,dataset6_fixed))
            elif loc == 7:
                dataset7 =  dataset7[~np.all(dataset7 == 0, axis=1)]
                dataset7_fixed = matcher.surface_match(dataset1_new,dataset7)
                dataset1_new = np.vstack((dataset1_new,dataset7_fixed))
            elif loc == 8:
                dataset8 =  dataset8[~np.all(dataset8 == 0, axis=1)]
                dataset8_fixed = matcher.surface_match(dataset1_new,dataset8)
                dataset1_new = np.vstack((dataset1_new,dataset8_fixed))
            elif loc == 9:
                dataset9 =  dataset9[~np.all(dataset9 == 0, axis=1)]
                dataset9_fixed = matcher.surface_match(dataset1_new,dataset9)
                dataset1_new = np.vstack((dataset1_new,dataset9_fixed))
            else:
                datasetmisc =  datasetmisc[~np.all(datasetmisc == 0, axis=1)]
                datasetmisc_fixed = matcher.surface_match(dataset1_new,datasetmisc)
                dataset1_new = np.vstack((dataset1_new,datasetmisc_fixed))

        return dataset1_new

    def filtering(self):
        rows = []
        for row in self.fixed_data:
            rows.append(row)
        L = [float(row[0]) for row in rows]
        X = [float(row[1]) for row in rows]
        Y = [float(row[2]) for row in rows]
        Z = [float(row[3]) for row in rows]
        X_n = np.array(X)
        Y_n = np.array(Y)
        Z_n = np.array(Z)

        first_pass_data = FWOCFM.FWOCFM(Z_n)

        second_pass_data = TDLS.TDLS(X_n,Y_n,first_pass_data)

        filt_data = np.concatenate(([X_n], [Y_n], [second_pass_data]))
        filt_data = np.transpose(filt_data)

        print('DATA FILTER COMPLETE!')
        self.finished = 1

        return filt_data

    def uncertainty(self):
        rows1 = []
        rows2 = []
        for row1 in self.data:
            rows1.append(row1)
        Z =  [float(row1[3]) for row1 in rows1]
        dx = [float(row1[4]) for row1 in rows1]
        dy = [float(row1[5]) for row1 in rows1]
        dz = [float(row1[5]) for row1 in rows1]
        for row2 in self.filt_data:
            rows2.append(row2)
        Z_o =[float(row2[2]) for row2 in rows2]
        Z_o = np.asarray(Z_o)

        u_z = np.abs(self.fixed_data[:,3]-Z) + dz
        delt = np.concatenate(([dx],[dy],[u_z]))
        delt = np.transpose(delt)
        print(delt)

        return delt