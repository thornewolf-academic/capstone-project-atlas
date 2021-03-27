import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import math
import matcher
import pandas as pd

data = np.load('sim_loc_data.npy')
L = np.asarray(data[:,0])
X = np.asarray(data[:,1])
Y = np.asarray(data[:,2])
Z = np.asarray(data[:,3])
dataset1 = np.zeros([len(L),4])
dataset2 = np.zeros([len(L),4])
dataset3 = np.zeros([len(L),4])

for i in range(0,len(L)):
    if data[i,0] == 1:
        dataset1[i,:] = data[i,:]
    elif data[i,0] == 2:
        dataset2[i,:] = data[i,:]
    elif data[i,0] == 3:
        dataset3[i,:] = data[i,:]
dataset1 =  dataset1[~np.all(dataset1 == 0, axis=1)]
dataset2 =  dataset2[~np.all(dataset2 == 0, axis=1)]
dataset3 =  dataset3[~np.all(dataset3 == 0, axis=1)]

dataset2_fixed = matcher.surface_match(dataset1,dataset2)
print(dataset1)
print(dataset2_fixed)
dataset1_new = np.vstack((dataset1,dataset2_fixed))
dataset3_fixed = matcher.surface_match(dataset1_new,dataset3)
dataset1_new = np.vstack((dataset1_new,dataset3_fixed))


fig = plt.figure()
ax1 = fig.gca(projection ="3d")
ax1.set_aspect('auto')
ax1.scatter(dataset1[:,1],dataset1[:,2],dataset1[:,3],c='b',marker="s",label='Localized Scan 1')
ax1.scatter(dataset2[:,1],dataset2[:,2],dataset2[:,3],c='r',marker="s",label='Localized Scan 2')
ax1.scatter(dataset3[:,1],dataset3[:,2],dataset3[:,3],c='g',marker="s",label='Localized Scan 3')
plt.legend(loc='upper left')
ax1.axes.set_xlim3d(left=-1000, right=1000) 
ax1.axes.set_ylim3d(bottom=-1000, top=1000) 
ax1.axes.set_zlim3d(bottom=-1000, top=1000) 
ax1.set_xlabel('x (cm)')
ax1.set_ylabel('y (cm)')
ax1.set_zlabel('z (cm)')

fig = plt.figure()
ax1 = fig.gca(projection ="3d")
ax1.set_aspect('auto')
ax1.scatter(dataset1_new[:,1],dataset1_new[:,2],dataset1_new[:,3],c='b',marker="s",label='Fixed Localization')
plt.legend(loc='upper left')
ax1.axes.set_xlim3d(left=-1000, right=1000) 
ax1.axes.set_ylim3d(bottom=-1000, top=1000) 
ax1.axes.set_zlim3d(bottom=-1000, top=1000) 
ax1.set_xlabel('x (cm)')
ax1.set_ylabel('y (cm)')
ax1.set_zlabel('z (cm)')

pd.DataFrame(dataset1_new).to_csv("fixed_data_set.csv")

plt.show()