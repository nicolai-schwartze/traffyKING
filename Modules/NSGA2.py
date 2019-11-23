# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:08:37 2019

@author: Nicolai
"""

import numpy as np
import copy


class individual:
    fList = list()
    xArray = np.array([])
    dominationCount = 0
    dominates = list()
    rank = 0
    distance = 0


def fast_non_dominated_sort(population):
    Rt = copy.deepcopy(population)
    popSize = len(Rt)
    searchDim = Rt[0].xArray.shape[0]
    solutionDim = len(Rt[0].fList)
    
    # set up population list
    for i in range(popSize):
        Rt[i].dominationCount = 0
        Rt[i].dominates = list()
    
    # check if i dominates j
    for i in range(popSize):
        for j in range(popSize):
            if (i == j): 
                continue
            else:
                # domination equation
                # (x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)
                # (domListSmallerOrEqual) and (domListSmaller)
                domListSmallerOrEqual = list()
                domListSmaller = list()
                for k in range(solutionDim):
                    if (Rt[i].fList[k] <= Rt[j].fList[k]):
                        domListSmallerOrEqual.append(True)
                    else:
                        domListSmallerOrEqual.append(False)
                    if (Rt[i].fList[k] < Rt[j].fList[k]):
                        domListSmaller.append(True)
                    else:
                        domListSmaller.append(False)
                    
                if ((not (False in domListSmallerOrEqual)) and (True in domListSmaller)):
                    Rt[j].dominationCount = Rt[j].dominationCount + 1
                    Rt[i].dominates.append(j)
    
    # create list of fronts
    tempRt= copy.deepcopy(Rt)
    fronts = list()
    
    for k in range(len(Rt)):
        tempFront = list()
        tempSubtractOneList = list()
        for i in range(len(tempRt)):
            if tempRt[i].dominationCount == 0:
                Rt[i].rank = k
                tempFront.append(Rt[i])
                tempRt[i].dominationCount = -1
                tempSubtractOneList.extend(tempRt[i].dominates)
        
        for i in tempSubtractOneList:
            tempRt[i].dominationCount = tempRt[i].dominationCount -1
        
        if not (len(tempFront) == 0):
            fronts.extend(tempFront)
        
    return copy.deepcopy(fronts)



def crowding_distance_sorting(Rt, Pt_size):
    Rt = copy.deepcopy(Rt)
    Pt = list()
    populationIsFull = False
    
    frontsCounter = list()
    for i in range(len(Rt)):
        frontsCounter.append(Rt[i].rank)
        
    for i in range(max(frontsCounter)+1):
        
        I = list()
        firstIndex = frontsCounter.index(i)
        lastIndex = firstIndex + frontsCounter.count(i)
        for j in range(firstIndex, lastIndex):
            I.append(copy.deepcopy(Rt[j]))
            
        # set crowding distance
        for o in range(len(I[0].fList)):
            # sort by objective
            I.sort(key=lambda s: s.fList[o])
            # set boundy distance to infinity
            I[0].distance = np.inf
            I[-1].distance = np.inf
            # calculate all other distances
            for k in range(1,len(I)-1):
                I[k].distance = I[k].distance + \
                (I[k+1].fList[o] - I[k-1].fList[o])/(I[-1].fList[o] - I[0].fList[o])
                    
        
        I.sort(key=lambda d: d.distance, reverse=True)
        for j in range(len(I)):
            # append the crowding sorted Individuals to reach Pt_size
            Pt.append(I[j])
            if (len(Pt) == Pt_size):
                populationIsFull = True
                break
        
        if populationIsFull:
            break
        
    return Pt


def mutation(O):
    O = copy.deepcopy(O)
    index = np.random.choice(len(O.xArray))
    factor = np.random.normal()
    O.xArray[index] = O.xArray[index] + factor * O.xArray[index]
    
    return O


def crossover(P):
    O = list()
    
    O.append(individual())
    O.append(individual())
    
    for i in range(len(P[0].xArray)):
        if np.random.randint(0,1) == 0:
            O[0].xArray = np.append(O[0].xArray, P[0].xArray[i])
            O[1].xArray = np.append(O[1].xArray, P[1].xArray[i])
        else:
            O[0].xArray = np.append(O[0].xArray, P[1].xArray[i])
            O[1].xArray = np.append(O[1].xArray, P[0].xArray[i])

    return O


def tournamentSelection(Pt):
    Pt = copy.deepcopy(Pt)
    pIndizes = np.random.choice(len(Pt), 4)
    
    M = list()
    
    if Pt[pIndizes[0]].rank < Pt[pIndizes[1]].rank:
        M.append(Pt[pIndizes[0]])
    elif Pt[pIndizes[0]].rank > Pt[pIndizes[1]].rank:
        M.append(Pt[pIndizes[1]])
    else:
        if Pt[pIndizes[0]].distance > Pt[pIndizes[1]].distance:
            M.append(Pt[pIndizes[0]])
        else:
            M.append(Pt[pIndizes[1]])
            
    if Pt[pIndizes[2]].rank < Pt[pIndizes[3]].rank:
        M.append(Pt[pIndizes[2]])
    elif Pt[pIndizes[2]].rank > Pt[pIndizes[3]].rank:
        M.append(Pt[pIndizes[3]])
    else:
        if Pt[pIndizes[2]].distance > Pt[pIndizes[3]].distance:
            M.append(Pt[pIndizes[2]])
        else:
            M.append(Pt[pIndizes[3]])
    
    return M


def NSGA2 (population, function, maxGeneration=1000000):
    Pt = copy.deepcopy(population)   
    parentPopulationSize = len(Pt)
    generationCounter = 0
    fDynamic = []
    
    while generationCounter < maxGeneration:
        # create offspring
        Qt = list()
        for i in range(int(len(Pt)/2)):
            # select two parents
            p = tournamentSelection(Pt)
            # crossover takes two parents and returns two offspring
            q = crossover(p)
            # mutation takes one offspring and modifies that
            q[0] = mutation(q[0])
            q[1] = mutation(q[1])
            # evaluate individual with function
            q[0].fList = function(q[0].xArray)
            q[1].fList = function(q[1].xArray)
            Qt.append(copy.deepcopy(q[0]))
            Qt.append(copy.deepcopy(q[1]))
        
        Rt = copy.deepcopy(Pt)
        Rt.extend(copy.deepcopy(Qt))
        
        # reset deminationCount, dominates, rank and distance
        for i in range(len(Rt)):
            Rt[i].dominationCount = 0
            Rt[i].dominates = list()
            Rt[i].rank = 0
            Rt[i].distance = 0
    
        # sort Rt by domination into fronts
        Rt = fast_non_dominated_sort(Rt)
        
        # generate new parent population ranked by crowding distance
        Pt = crowding_distance_sorting(Rt, parentPopulationSize)
        for p in Pt:
            fDynamic.append(p.fList)
            
        generationCounter = generationCounter + 1

    return Pt, fDynamic


def populationInitialisation(function, populationSize, lowerBound, upperBound):
    problemSize = len(lowerBound)
    Pt = list()
    for i in range(populationSize):
        tempIndividual = np.array([])
        for j in range(problemSize): 
            tempX = np.random.uniform(low=lowerBound[j], high=upperBound[j])
            tempIndividual = np.append(tempIndividual, tempX)
        
        I = individual()
        I.xArray = tempIndividual
        f = function(tempIndividual)
        I.fList = f
        Pt.append(I)
        
    return Pt



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    def singleSphere(x):
        return np.dot(x,x)
    
    def multiSphere (x): 
        r1 = singleSphere(x - 4)
        r2 = singleSphere(x + 4)
        return [r1, r2]
    
    print("start test: fast_non_dominated_sort")
    print(50*"=")
    print()
    
    points = [[0, 40], [2, 33], [5, 29], [8, 14], [10, 0], \
              [3, 50], [7, 35], [9, 30], [14, 14], [17, 5], \
              [1, 60], [4, 60], [6, 53], [10, 45], [12, 40], \
              [14, 37], [18, 31], [15, 50], [17, 45], [20, 40]]
    
    testPopulation = list()
    for i in range(len(points)):
        testPopulation.append(individual())
        testPopulation[i].fList = points[i]
        testPopulation[i].xArray = np.random.randint(0, 10, 5)
        
        
    solutionPopulation = fast_non_dominated_sort(testPopulation)
    
    for i in range(len(solutionPopulation)):
        if solutionPopulation[i].rank == 0:
            plt.plot(solutionPopulation[i].fList[0], \
                 solutionPopulation[i].fList[1], \
                 marker='o', color='r', ls='')
        if solutionPopulation[i].rank == 1:
            plt.plot(solutionPopulation[i].fList[0], \
                 solutionPopulation[i].fList[1], \
                 marker='o', color='g', ls='')
        if solutionPopulation[i].rank == 2:
            plt.plot(solutionPopulation[i].fList[0], \
                 solutionPopulation[i].fList[1], \
                 marker='o', color='b', ls='')
        if solutionPopulation[i].rank == 3:
            plt.plot(solutionPopulation[i].fList[0], \
                 solutionPopulation[i].fList[1], \
                 marker='o', color='y', ls='')
            
    plt.show()
            
            
        
    
    for i in range(len(solutionPopulation)):
        print("individual " + str(i))
        print("--------------------")
        print("rank: " + str(solutionPopulation[i].rank))
        print("dominationCount: " + str(solutionPopulation[i].dominationCount))
        print("dominates: " + str(solutionPopulation[i].dominates))
        print()
        print()
        
    assert (len(testPopulation) == len(solutionPopulation)), "test and solution population not of same length"
    Pt = crowding_distance_sorting(solutionPopulation, 10)
    # ToDo What happens with fronts that have less individual (eg. 1, 2, 3)
    
    p1, p2 = tournamentSelection(Pt)
    
    testPopulation = populationInitialisation(multiSphere, 100, [-10, -10], [10, 10])
    OP = NSGA2(testPopulation, multiSphere, maxGeneration=1000)
    for i in range(len(OP)):
        if OP[i].rank == 0:
            plt.plot(OP[i].fList[0], \
                 OP[i].fList[1], \
                 marker='o', color='r', ls='')
        if OP[i].rank == 1:
            plt.plot(OP[i].fList[0], \
                 OP[i].fList[1], \
                 marker='o', color='g', ls='')
        if OP[i].rank == 2:
            plt.plot(OP[i].fList[0], \
                 OP[i].fList[1], \
                 marker='o', color='b', ls='')
        if OP[i].rank == 3:
            plt.plot(OP[i].fList[0], \
                 OP[i].fList[1], \
                 marker='o', color='y', ls='')
            
    plt.show()
    print()
    print("test passed")
    
        
    
    
    
    
    





