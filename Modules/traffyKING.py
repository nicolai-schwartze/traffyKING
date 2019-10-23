# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:52:27 2019

@author: Nicolai
"""

from bs4 import BeautifulSoup
import numpy as np
from sumolib import checkBinary  
import traci  
import sys

def evaluate_Simulation_Multicriteria(tripinfoFile):
    ''' 
    
    input  : tripinfo file as created by a sumo simulation 
    
    output : a tuple of the three separate optimisation criterias
    
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
        waitingtimeList.append(float(info["waitingtime"]))
        stopCount = stopCount + int(info["waitingcount"])
    
    waitingtime = np.mean(waitingtimeList)
    fairness = np.var(waitingtimeList)
    
    return (waitingtime, stopCount, fairness)



def evaluate_Simulation_Singlecriteria(tripinfoFile, weightWT=5, weightSC=1, weightF=5):
    ''' 
    
    input  : tripinfo file as created by a sumo simulation 
    
    output : a weighted sum of the criteria waitingtime, stopcount and fairness
             calculated by (waitingtime + stopcount + fairness)/3
        
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
        waitingtimeList.append(float(info["waitingtime"]))
        stopCount = stopCount + int(info["waitingcount"])
    
    waitingtime = np.mean(waitingtimeList)
    fairness = np.var(waitingtimeList)
    
    return (waitingtime*weightWT + stopCount*weightSC + fairness*weightF)/3



def start_Simulation():
    sumoBinary = checkBinary('sumo')
    
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    
    
# Edit this from tutorial
# need to call simulation from string
def run():
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("0", 2)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if traci.trafficlight.getPhase("0") == 2:
            # we are not already switching
            if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
                # there is a vehicle from the north, switch
                traci.trafficlight.setPhase("0", 3)
            else:
                # otherwise try to keep green for EW
                traci.trafficlight.setPhase("0", 2)
        step += 1
    traci.close()
    sys.stdout.flush()



if __name__ == "__main__": 
    wT_List = [0, 2, 1, 4, 0, 2, 4, 4] 
    sC_List = [0, 1, 1, 2, 0, 2, 2, 3]
    print("start test")
    print(50*"=")
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
    
    
