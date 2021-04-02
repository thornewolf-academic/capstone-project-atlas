# ATLAS -- Noise Filtering Software Version 1.0
# Main script 
# Make this a class file with begin and done functions 

import numpy as np
from uncertainties import unumpy as unp
from uncertainties import umath
import uncertainties 
import numpy as np
import matplotlib.pyplot as plt 
import csv
from mpl_toolkits.mplot3d import Axes3D
import scipy.integrate as integrate
import scipy.special as special
import FWOCFM 
import TDLS
 
 
rows = []
 
with open('more point scan 3.17.TXT', 'r') as csvfile:
    coordinates = csv.reader(csvfile, delimiter=',')
    for row in coordinates:
        rows.append(row)
 
#print(rows)
X = [float(row[0]) for row in rows]
Y = [float(row[1]) for row in rows]
Z = [float(row[2]) for row in rows]
X_n = np.array(X)
Y_n = np.array(Y)
Z_n = np.array(Z)

#filter noise
first_pass_data = FWOCFM.FWOCFM(Z_n)

second_pass_data = TDLS.TDLS(X_n,Y_n,first_pass_data)
print('')
print('Filtered Data:')
print(second_pass_data)


fig = plt.figure()
ax1 = fig.gca(projection ="3d")
ax1.set_aspect('auto')
ax1.scatter(X, Y, Z,c='b',marker="s", label='raw data')  
plt.legend(loc='upper left')
ax1.set_xlim3d(-600, 600)
ax1.set_xlabel('x (cm)')
ax1.set_ylim3d(-700,500)
ax1.set_ylabel('y (cm)')
ax1.set_zlim3d(0,600)
ax1.set_zlabel('z (cm)')
fig = plt.figure()
ax2 = fig.gca(projection = "3d")
ax2.set_aspect('auto')
ax2.scatter(X_n,Y_n,second_pass_data,c='r',marker="s",label='filtered data')
plt.legend(loc='upper left')
ax1.set_xlim3d(-600, 600)
ax2.set_xlabel('x (cm)')
ax2.set_ylim3d(-700,500)
ax2.set_ylabel('y (cm)')
ax2.set_zlim3d(0,600)
ax2.set_zlabel('z (cm)')

# ax.set_xlabel('safas')
plt.grid()
plt.show()