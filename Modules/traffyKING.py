# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:52:27 2019

@author: Nicolai
"""

from bs4 import BeautifulSoup
import numpy as np
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



def evaluate_Simulation_Singlecriteria(tripinfoFile, weightWT=5, weightSC=1, weightF=5):
    ''' 
    input  : tripinfo file as created by a sumo simulation 
    
    output : a weighted sum of the criteria waitingtime, stopcount and fairness
             calculated by (waitingtime + stopcount + fairness)/3
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
    
    return list([(waitingtime*weightWT + stopCount*weightSC + fairness*weightF)/3])


def simulation_Runner(simulationSteps):
    n = 0
    while(n < simulationSteps):
        traci.simulationStep()
        n = n + 1
    
    traci.close()
    sys.stdout.flush()
    
    

if __name__ == "__main__": 
    
    print("start test")
    print(50*"=")
    
    wT_List = [0, 2, 1, 4, 0, 2, 4, 4] 
    sC_List = [0, 1, 1, 2, 0, 2, 2, 3]
    wT, sC, F = evaluate_Simulation_Multicriteria("test_Tripinfo.xml")
    print("waitingtime = " + str(wT))
    print("number of stops = " + str(sC))
    print("fairness = " + str(F))
    assert (np.mean(wT_List) == wT) 
    assert (np.var(wT_List) == F)
    assert (np.sum(sC_List) == sC)
    result = evaluate_Simulation_Singlecriteria("test_Tripinfo.xml")
    print("weighted result = " + str(result))
    assert (result == (np.mean(wT_List)*5 + np.var(wT_List)*5 + np.sum(sC_List))/3)
    print("test passed")
    
    
