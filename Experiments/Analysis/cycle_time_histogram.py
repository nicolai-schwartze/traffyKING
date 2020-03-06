# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 20:46:09 2020

@author: Nicolai
"""


import pickle
import matplotlib.pyplot as plt
import numpy as np
import sys
import pickle

sys.path.append('../../Modules')
import NSGA2


print("read last result")
with open('../exp_3x3_night_nsga2/data_backup/NSGA2_SaveList_g8_g14.pkl', 'rb') as pickle_file:
    backup = pickle.load(pickle_file)
    
    
xArray = []
fList = []

for i in range(0, len(backup[-1][0])):
    asdf = backup[-1][0][i].xArray
    bsdf = np.array([0, asdf[1], asdf[1], asdf[1], asdf[1], asdf[1], asdf[1], asdf[1], asdf[1], asdf[1]])
    csdf = (asdf - bsdf)
    csdf[1] = 0.0
    xArray.append(csdf.tolist())
    
for i in range(0, len(backup[-1][0])):
    fList.append(backup[-1][0][i].fList)
    
cycleTimeHist = []
for i in xArray:
    cycleTimeHist.append(i[0])
    
n, bins, patches = plt.hist(cycleTimeHist, 10, density=True, facecolor='g', alpha=0.75)
plt.xlabel('green time per cycle')
plt.ylabel('distribution')
plt.title('Green Time Distribution in NSGA-II Gen 19 Night Scenario')
plt.grid(True)
plt.show()