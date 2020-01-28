# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 23:33:44 2020

@author: Nicolai
----------------
"""


from __future__ import absolute_import
from __future__ import print_function

import sys
import pickle

sys.path.append('../../Modules')
import NSGA2

import Cross_3_3_night as c33


if __name__ == "__main__":
    
    # calculating
    # print("start init random")
    # pop = NSGA2.populationInitialisationNSGA2(c33.function_Cross_3_3, 30, [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [70, 70, 70, 70, 70, 70, 70, 70, 70, 70])
    print("read old pop")
    with open('NSGA2_SaveList.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    pop = backup[-1][0]
    print("finished init")
    opt4, fD4 = NSGA2.NSGA2(pop, c33.function_Cross_3_3, maxGeneration=6)
        
        
        
        
    # plotting 3D Scatter
    # from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
    # import matplotlib.pyplot as plt
    # with open('NSGA2_SaveList.pkl', 'rb') as pickle_file:
    #     backup = pickle.load(pickle_file)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # plotPoints = backup[-1][1][-30:]
    # for x, y, z in plotPoints:
    #     print(str(x) + " " + str(y) + " " + str(z))
    #     ax.scatter(x, y, z)

    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')
    
    # plt.show()
