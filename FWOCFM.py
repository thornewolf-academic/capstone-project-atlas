# ATLAS -- Noise Filtering Software Version 1.0
#Fuzzy-Weighted Optimum Curve Fit Method of Noise Filtering 
#First leg of the noise filtering process

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

def FWOCFM(data):
        #----------------------------------------------------------------------------------------------
        #FUNCTION BEGINS HERE
        bar = progressbar.ProgressBar(maxval=10, \
                widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        print('FWOCFM progerss:')
        bar.start()

        for y in range (0,10):
                bar.update(y+1)
                if y == 0:
                        Cs = 1 
                        Cv = 45
                        fun = pd.to_numeric(data)
                else:
                        Cs = 1
                        Cv = Cv + 10*y
                        fun = pd.to_numeric(fuzzies)
                oof = np.ones(len(fun))
                xbar = sum(fun)/len(fun)
                a0 = xbar*(1-((2*Cv)/Cs))
                beta = 2/(xbar*Cv*Cs)
                alpha = 4/(Cs^2)
                exponent  = (alpha-1)*np.exp(np.float(beta)*(fun - np.float(a0)))
                base = np.abs(beta)/math.gamma(alpha)*(beta*(fun - a0))
                P = np.power(base, exponent)
                for u in range(0,len(P)):
                        if P[u] == complex():
                                P[u] = 0
                        elif math.isnan(P[u]):
                                P[u] = 0
                        elif math.isinf(P[u]):
                                P[u] = 0
                Phi = (Cs/2)*invgamma.rvs(1-P,alpha) - (2/Cs)
                for v in range(0,len(Phi)):
                        if Phi[v] == complex():
                                Phi[v] = 0
                        elif math.isnan(Phi[v]):
                                Phi[v] = 0
                        elif math.isinf(Phi[v]):
                                P[v] = 0
                x_pm = xbar*(1+Cv*(Phi))
                sig_m = np.std(x_pm)
                X = (fun-x_pm)/(math.sqrt(2)*sig_m)
                S = np.std(X)
                n = len(X)
                B = S/(math.sqrt(n)*sig_m)
                a = np.array([None] * len(fun),dtype=np.float64)
                b = np.array([None] * len(fun),dtype=np.float64)
                FW_m = np.array([None] * len(fun),dtype=np.float64)
                fuzzies = np.array([None] * len(fun))
                for j in range(0,len(fun)):
                        a[j] = (fun[j] + B - x_pm[j])/(math.sqrt(2)*sig_m)
                        b[j] = (fun[j] - B - x_pm[j])/(math.sqrt(2)*sig_m)
                        def integrand(X):
                                return -X**2
                        FW_m = (fun[j] - (np.int(10000/(6.28)))*((scipy.integrate.quad(integrand,a[j],b[j]))))
                        fuzz = FW_m[0]
                        fuzzies[j] = fuzz
        bar.finish()
        return fuzzies
#FUNCTION ENDS HERE
#---------------------------------------------------------------------------------------------------