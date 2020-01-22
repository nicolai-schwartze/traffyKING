# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
    with open('../exp_3x3_day_nsga2/data_backup/NSGA2_SaveList_g0_g1.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup[0])):
        populations.append(copy.deepcopy(backup[0][i][0]))
    with open('../exp_3x3_day_nsga2/data_backup/NSGA2_SaveList_g2_g6.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup[0])):
        populations.append(copy.deepcopy(backup[0][i][0]))
    with open('../exp_3x3_day_nsga2/data_backup/NSGA2_SaveList_g7_g8.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup[0])):
        populations.append(copy.deepcopy(backup[0][i][0]))
    with open('../exp_3x3_day_nsga2/data_backup/NSGA2_SaveList_g9_g16.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup[0])):
        populations.append(copy.deepcopy(backup[0][i][0]))
    with open('../exp_3x3_day_nsga2/data_backup/NSGA2_SaveList_g17_g18.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup[0])):
        populations.append(copy.deepcopy(backup[0][i][0]))
    with open('../exp_3x3_day_nsga2/data_backup/NSGA2_SaveList_g19_g20.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup[0])):
        populations.append(copy.deepcopy(backup[0][i][0]))
    generations = len(populations)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plotPoints = backup[0][1][-30:]
    for x, y, z in plotPoints:
        print(str(x) + " " + str(y) + " " + str(z))
        ax.scatter(x, y, z)

    ax.set_xlabel('Waitingtime')
    ax.set_ylabel('Stopcount')
    ax.set_zlabel('Fairness')
    
    plt.show()































