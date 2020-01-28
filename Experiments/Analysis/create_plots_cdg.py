# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:19:40 2020

@author: Nicolai
----------------
"""

if __name__ == "__main__": 
    import pickle
    import sys
    sys.path.append('../../Modules')
    import NSGA2
    import copy 
        
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
    import matplotlib.pyplot as plt
    populations = []
    with open('../exp_3x3_night_cgd/data_backup/CGD_SaveList_i0_i7.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    
    
    iterations = len(populations)
    
    fig = plt.figure(figsize=(13,8))
    ax = fig.add_subplot(111)
        
    ax.plot(backup[-1][-1])
        
    ax.set_xlabel('iterations')
    ax.set_ylabel('function value')
    ax.set_title("Conjugate Gradient Descent Night")
    plt.savefig("exp_3x3_night_cgd/cgd_night.png")
    plt.show()































