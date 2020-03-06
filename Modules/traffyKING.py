# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:52:27 2019

@author: Nicolai
"""

from bs4 import BeautifulSoup
import numpy as np
import csv
import traci  
import sys

def evaluate_Simulation_Multicriteria(tripinfoFile):
    ''' 
    input  : tripinfo file as created by a sumo simulation 
    
    output : a list of the three separate optimisation criterias
             the parameters are normalised by the routlenght of each car
             this is necessary since a longer route causes more stops and
             thus a longer waiting time
    
                waitingtime: mean over all times all cars have waited
                stopCount  : number of stops all cars had to perform
                fairness   : variance of the waitingtime 
    '''
    

    with open(tripinfoFile) as result:
        content = result.readlines()
    
    xmlString = ""
    xmlString = xmlString.join(content)
    
    xml = BeautifulSoup(xmlString, features="lxml")
    infos = xml.tripinfos.findAll("tripinfo")
    
    waitingtimeList = []
    stopCount = 0
    
    for info in infos:
        routLength = float(info["routelength"])
        waitingtimeList.append(float(info["waitingtime"])/routLength)
        stopCount = stopCount + int(info["waitingcount"])/routLength
        
    
    waitingtime = np.mean(waitingtimeList)
    fairness = np.var(waitingtimeList)
    
    return list([waitingtime, stopCount, fairness])



def evaluate_Simulation_Singlecriteria(tripinfoFile, weightWT=1, weightSC=1, weightF=1):
    ''' 
    input  : tripinfo file as created by a sumo simulation 
    
    output : a weighted sum of the criteria waitingtime, stopcount and fairness
             calculated by: 
             (weightWT*waitingtime + weightSC*stopcount + weightF*fairness)
             ---------------------------------------------------------------
             (weightWT + weightSC + weightF)
             the parameters are normalised by the routlenght of each car
             this is necessary since a longer route causes more stops and
             thus a longer waiting time
    '''
    

    with open(tripinfoFile) as result:
        content = result.readlines()
    
    xmlString = ""
    xmlString = xmlString.join(content)
    
    xml = BeautifulSoup(xmlString, features="lxml")
    infos = xml.tripinfos.findAll("tripinfo")
    
    waitingtimeList = []
    stopCount = 0
    
    for info in infos:
        routLength = float(info["routelength"])
        waitingtimeList.append(float(info["waitingtime"])/routLength)
        stopCount = stopCount + int(info["waitingcount"])/routLength
    
    waitingtime = np.mean(waitingtimeList)
    fairness = np.var(waitingtimeList)
    
    return list([(waitingtime*weightWT + stopCount*weightSC + fairness*weightF)/(weightWT + weightSC + weightF)])
   
def simulation_Runner(simulationSteps):
    n = 0
    while(n < simulationSteps):
        traci.simulationStep()
        n = n + 1
    
    traci.close()
    sys.stdout.flush()
    
    
def calculateRelativeGreenFromFile(fileName, numberOfCrosses):
    
    turnProbability = [0.25, 0.5, 0.25]
    
    characterList = ['A', 'D', 'B', 'C']
    inputList = [];
    
    with open(fileName) as f:
        contentSTR = f.readlines()
    
    with open(fileName) as f:
        contentCSV = csv.reader(f,delimiter=';')
        csvList = list(contentCSV)
    
    for c in range(1, (numberOfCrosses+1)**2):
        tempList = []
        for ch in characterList:
            lineCounter = 0
            for l in contentSTR:
                if ("i" + str(c) + ch) in l:
                    tempList.append(float(csvList[lineCounter][1].replace(',','.')))
                lineCounter = lineCounter + 1;
        if not (len(tempList) == 0):
            inputList.append(tempList)
        
    returnList = []
            
    for i in range(len(inputList)):
        u1 = inputList[i][0] * (0.25 + 0.5)
        u2 = inputList[i][2] * (0.25 + 0.5)
        v1 = max(u1, u2)
        
        u3 = inputList[i][0] * (0.25)
        u4 = inputList[i][2] * (0.25)
        v2 = max(u3, u4)
                
        u5 = inputList[i][1] * (0.5 + 0.25)
        u6 = inputList[i][3] * (0.5 + 0.25)
        v3 = max(u5, u6)
                
        u7 = inputList[i][3] * (0.25)
        u8 = inputList[i][1] * (0.25)
        v4 = max(u7, u8)
                
        denominator = v1 + v2 + v3 + v4
        returnList.append([v1/denominator, v2/denominator, v3/denominator, v4/denominator])
           
    return returnList
    

if __name__ == "__main__": 
    
    print("start test")
    print(50*"=")
    
    wT, sC, F = evaluate_Simulation_Multicriteria("test_Tripinfo2.xml")
    print("waitingtime = " + str(wT))
    print("number of stops = " + str(sC))
    print("fairness = " + str(F))
    
    result = evaluate_Simulation_Singlecriteria("test_Tripinfo.xml")
    print("weighted result = " + str(result))
    
    rG = calculateRelativeGreenFromFile("Cross3x3LP.csv", 9)
    print(rG)
    
    print("test passed")
    
    
    
    
