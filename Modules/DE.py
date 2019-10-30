# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 10:30:04 2019

@author: Nicolai Schwartze
"""

import numpy as np


def crossoverBIN(xi, vi, CR):
    r, c = vi.shape
    K = np.random.randint(low=0, high=c)
    ui = []
    for j in range(c):
        if j==K or np.random.rand() < CR:
            ui.append(vi[0][j])
        else:
            ui.append(xi[0][j])
    return np.asarray(ui)


def mutationRand1(population, populationByIndex, currentIndex, bestIndex, F):
    indizes = populationByIndex[:]
    indizes.remove(currentIndex)
    indizes = np.random.permutation(indizes)
    r0 = np.array([population[indizes[0]]])
    r1 = np.array([population[indizes[1]]])
    r2 = np.array([population[indizes[2]]])
    vi = r0 + F*(r1-r2)
    return vi


def DifferentialEvolution(population, function, maxFunctionEval=10000, F=0.5, CR=0.1):
    populationSize, dimension = population.shape
    populationByIndex = list(range(0, populationSize))
    functionValue = np.asarray([function(candidate) for candidate in population])
    functionEvalCounter = populationSize
    bestCandidateIndex = np.argmin(functionValue)

    while(functionEvalCounter < maxFunctionEval):
        for i in range(populationSize):
            vi = mutationRand1(population, populationByIndex, i, bestCandidateIndex, F)
            ui = crossoverBIN(np.array([population[i]]), vi, CR)
            tempFuncValue = function(ui)
            functionEvalCounter = functionEvalCounter + 1
            if(tempFuncValue < functionValue[i]):
                population[i] = ui
                functionValue[i] = tempFuncValue
        bestCandidateIndex=np.argmin(functionValue)

    return population[bestCandidateIndex]


if __name__ == "__main__":
    print("start test")
    print(50*"=")
    
    def sphere(x):
        return np.dot(x,x)
    
    testPopulation = np.random.rand(20,2)*np.random.randint(-1000, 1000)
    
    print(DifferentialEvolution(testPopulation, sphere))


