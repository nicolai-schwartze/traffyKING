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
    with open('../exp_3x3_night_nsga2/data_backup/NSGA2_SaveList_g0.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    with open('../exp_3x3_night_nsga2/data_backup/NSGA2_SaveList_g1.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    with open('../exp_3x3_night_nsga2/data_backup/NSGA2_SaveList_g2.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    with open('../exp_3x3_night_nsga2/data_backup/NSGA2_SaveList_g3_g6.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    with open('../exp_3x3_night_nsga2/data_backup/NSGA2_SaveList_g7.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    with open('../exp_3x3_night_nsga2/data_backup/NSGA2_SaveList_g8_g14.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    with open('../exp_3x3_day_nsga2/data_backup/NSGA2_SaveList_g15.pkl', 'rb') as pickle_file:
        backup = pickle.load(pickle_file)
    for i in range(len(backup)):
        populations.append(copy.deepcopy(backup[i][0]))
    
    
    generations = len(populations)
    
    for i in range(len(populations)):
        fig = plt.figure(figsize=(13,8))
        ax = fig.add_subplot(111, projection='3d')
        plotPoints = []
        for ind in populations[i]:
            plotPoints.append(ind.fList)
        for x, y, z in plotPoints:
            print(str(x) + " " + str(y) + " " + str(z))
            ax.scatter(x, y, z, )
        
        ax.view_init(30, 5*i)
        ax.set_xlabel('Waitingtime')
        ax.set_ylabel('Stopcount')
        ax.set_zlabel('Fairness')
        ax.set_title("Generation " + str(i))
        plt.savefig("exp_3x3_night_nsga2/nsga2_night_" + str(i) + ".png")
        plt.show()































