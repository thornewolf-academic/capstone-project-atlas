# ATLAS -- Noise Filtering Software Version 1.0
#F3D Least Squares Method of Noise Filtering 
#Second leg of the noise filtering process

import numpy as np
from uncertainties import unumpy as unp
from uncertainties import umath
import uncertainties 
import numpy as np
import matplotlib.pyplot as plt 
import csv
import numpy as np
import math
import scipy
from mpl_toolkits.mplot3d import Axes3D
import scipy.integrate as integrate
import scipy.special as special
from scipy.special import gamma, factorial
import math 
import scipy.integrate as integrate
import scipy.special as special
from scipy.stats import invgamma
import pandas as pd
import progressbar
from time import sleep

def TDLS(X,Y,data):
#----------------------------------------------------------------------------------------------
#FUNCTION BEGINS HERE
    bar = progressbar.ProgressBar(maxval=len(data)+10, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    print('3DLS progerss:')
    bar.start()

    for y in range (0,10):
        bar.update(y+1)
        if y == 0:
            search_surface = np.zeros(len(data))
        else:
            search_surface = fun
        a = np.linspace(-100,100,len(data))
        b = np.linspace(-100,100,len(data))
        dif = np.array([None] * len(data),dtype=np.float64)
        for i in range(0,len(data)):
            dif[i] = a[i] * (data[i]-search_surface[i])
        ind = (np.where(dif == np.min(dif)))
        aval = np.asscalar(a[ind])
        bval = np.asscalar(b[ind])
        fun = (aval+bval**2) * data
    scaling = np.max(data)/np.max(fun)
    filt = scaling*fun
    TDLS = np.array([None] * len(fun),dtype=np.float64)
    for u in range(0,len(X)):
        bar.update(u+1)
        for v in range(0,len(Y)):
            if np.abs(X[u] - X[v]) <= 0.1:
                TDLS[u] = (filt[u]+filt[v])/2
                TDLS[v] = (filt[u]+filt[v])/2
                #print('LOCALIZATION VARIATION DETECTED AND ADJUSTED')
            elif np.abs(Y[u] - Y[v]) <= 0.1:
                TDLS[u] = (filt[u]+filt[v])/2
                TDLS[v] = (filt[u]+filt[v])/2
                #print('LOCALIZATION VARIATION DETECTED AND ADJUSTED')
            elif np.abs(Y[u] - X[v]) <= 0.1:
                TDLS[u] = (filt[u]+filt[v])/2
                TDLS[v] = (filt[u]+filt[v])/2
                #print('LOCALIZATION VARIATION DETECTED AND ADJUSTED')
            elif np.abs(X[u] - Y[v]) <= 0.1:
                TDLS[u] = (filt[u]+filt[v])/2
                TDLS[v] = (filt[u]+filt[v])/2
                #print('LOCALIZATION VARIATION DETECTED AND ADJUSTED')
            else:
                TDLS[u] = filt[u]
    for i in range(5,len(TDLS)-5):
        nearby_points = np.array([TDLS[i-5],TDLS[i-4],TDLS[i-3],TDLS[i-2],TDLS[i-1],TDLS[i],TDLS[i+1],TDLS[i+2],TDLS[i+3],TDLS[i+4],TDLS[i+5]])
        mean_nearby_points = np.mean(nearby_points)
        if TDLS[i] >= 1.5*mean_nearby_points:
            TDLS[i] = np.mean(TDLS)
            print('OUTLIER DETECTED AND ADJUSTED')
        elif TDLS[i] <= 1.2*(np.mean(TDLS)):
            TDLS[i] = np.mean(TDLS)
        else:
            TDLS[i] = TDLS[i]
    bar.finish()
    return TDLS