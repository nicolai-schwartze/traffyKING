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
    fValue = []
    populations = []
    with open('../exp_3x3_day_hc/data_backup/HC_SaveList_g0_g7.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
        fValue = backup[-1][-1]
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    with open('../exp_3x3_day_hc/data_backup/HC_SaveList_g8_g27.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
        fValue.extend(backup[-1][-1])
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    
    
    iterations = len(populations)
    fValue_min = []
    f_before = 100
    for f in range(len(fValue)):
        if (fValue[f] < f_before):
            fValue_min.append(fValue[f])
            f_before = fValue[f]
        else:
            fValue_min.append(f_before)
            
    
    fig = plt.figure(figsize=(13,8))
    ax = fig.add_subplot(111)
        
    ax.plot(fValue, label='fValue')
    ax.plot(fValue_min, label='fValue_min')
        
    ax.set_xlabel('iterations')
    ax.set_ylabel('function value')
    ax.set_title("Hill Climbing Day")
    ax.legend()
    plt.savefig("exp_3x3_day_hc/hc_day.png")
    plt.show()






