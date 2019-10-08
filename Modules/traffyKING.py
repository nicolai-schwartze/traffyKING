# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:52:27 2019

@author: Nicolai
"""

from bs4 import BeautifulSoup
import numpy as np


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



def evaluate_Simulation_Singlecriteria(tripinfoFile):
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
    
    return (waitingtime + stopCount + fairness)/3



if __name__ == "__main__": 
    print(evaluate_Simulation_Multicriteria("test.xml"))
