# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 09:13:12 2019

@author: Nicolai
"""

import numpy as np

def hillClimbing(x, function, stepSize=1, functionEvaluation=10**5):
    dim = x.shape[-1]
    functionEvalCounter = 0
    oldFunctionValue = np.inf
    
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
        
        # if function value did improve
        if currentFunctionValue < oldFunctionValue:
            x = xList[minIndex]
            oldFunctionValue = currentFunctionValue
        # else adapt step size
        else:
            stepSize = stepSize*0.5

    return x
    


if __name__ == "__main__":
    
    def sphere(x):
        return np.dot(x,x)
    
    print("start test")
    opt = hillClimbing(np.array([34.23,-23.5,104.65,-1059,670.1,-340.3]), sphere)
    print(opt)
    
    print("passed test")