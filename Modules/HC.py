# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 09:13:12 2019

@author: Nicolai
"""

import numpy as np
import copy
import pickle
import matplotlib.pyplot as plt

def hillClimbing(x, function, stepSize=1, functionEvaluation=10**5):
    dim = x.shape[-1]
    functionEvalCounter = 0
    oldFunctionValue = np.inf
    fDynamic = []
    saveList = []
    iterationCounter = 0
    
    while (functionEvalCounter < functionEvaluation):
        # look around, create offspring
        xList = list()
        fList = list()
        for i in range(dim):
            # step in positive direction
            z = np.zeros(dim)
            z[i] = stepSize
            y = x + z
            xList.append(y)
            fList.append(function(y))
            functionEvalCounter = functionEvalCounter + 1
            # step in negative direction
            z = np.zeros(dim)
            z[i] = -stepSize
            y = x + z
            xList.append(y)
            fList.append(function(y))
            functionEvalCounter = functionEvalCounter + 1
            
        minIndex = np.argmin(fList)
        currentFunctionValue = fList[minIndex]
        fDynamic.append(currentFunctionValue)
        
        # if function value did improve
        if currentFunctionValue < oldFunctionValue:
            x = xList[minIndex]
            oldFunctionValue = currentFunctionValue
        # else adapt step size
        else:
            stepSize = stepSize*0.5
            
        saveList.append((copy.deepcopy(x), copy.deepcopy(fDynamic)))
        iterationCounter = iterationCounter + 1
        with open('HC_SaveList.pkl', 'wb') as f:
            pickle.dump(saveList, f)
        print("Iteration: " + str(iterationCounter))

    return x, fDynamic
    


if __name__ == "__main__":
    
    def sphere(x):
        return np.dot(x,x)
    
    print("start test")
    opt, fD = hillClimbing(np.array([34.23,-23.5]), sphere, functionEvaluation=500)
    print(opt)
    print(fD)
    
    plt.title("hill climbing on sphere function")
    plt.semilogy(fD)
    plt.xlabel("iteration")
    plt.ylabel("function value")
    
    print("passed test")