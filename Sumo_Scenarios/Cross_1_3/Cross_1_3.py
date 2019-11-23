
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import numpy as np
import inspect

sys.path.append('../../Modules')
import traffyKING as tk
import CGD
import DE
import HC
import NSGA2


# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci

def function_Cross_1_3(array):
    relativeGreen = np.array([[0.3,0.2,0.3,0.2],[0.3,0.1,0.5,0.1],[0.3,0.4,0.2,0.1]])
    periode = array[0]
    numberOfTrafficlights = 3
    
    generate_additional(array, periode, relativeGreen, numberOfTrafficlights)
    
    tempList = []
    for run in range(1,11):
        generate_routefile()
        
        sumoBinary = checkBinary('sumo')
        traci.start([sumoBinary, "-c", "Data/Cross_1_3.sumocfg",
                                 "--tripinfo-output", "tripinfo.xml"])
        tk.simulation_Runner(3600)
        
        singleResult = []
        if inspect.stack()[1].function == "NSGA2":
            singleResult = tk.evaluate_Simulation_Multicriteria("tripinfo.xml")
        else:
            singleResult = tk.evaluate_Simulation_Singlecriteria("tripinfo.xml")
            
        tempList.extend(singleResult)
        
    if inspect.stack()[1].function == "NSGA2":
        return np.mean(tempList, axis=0).tolist()
    else:
        return np.mean(tempList)


def generate_additional(array, periode, relativeGreen, numberOfTrafficlights):
    
    with open("Data/trafficLight.add.xml", "w") as additionals:
        print("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n" + "<additional>\n",file=additionals)
    
    for i in range(numberOfTrafficlights):
        green = (periode - 12)*relativeGreen[i,:]
        trafficLight = \
        "\t <tlLogic id=\"C%i\" type=\"static\" programID=\"1\" offset=\"%f\"> \n \
            <phase duration=\"%f\" state=\"GGgrrrGGgrrr\"/> \n \
            <phase duration=\"3\"  state=\"yygrrryygrrr\"/> \n \
            <phase duration=\"%f\" state=\"rrGrrrrrGrrr\"/> \n \
            <phase duration=\"3\"  state=\"rryrrrrryrrr\"/> \n \
            <phase duration=\"%f\" state=\"rrrGGgrrrGGg\"/> \n \
            <phase duration=\"3\"  state=\"rrryygrrryyg\"/> \n \
            <phase duration=\"%f\" state=\"rrrrrGrrrrrG\"/> \n \
            <phase duration=\"3\"  state=\"rrrrryrrrrry\"/> \n \
        </tlLogic> \n"

        with open("Data/trafficLight.add.xml", "a+") as additionals:
            print(trafficLight % (i+1, array[i+1], green[0], green[1],green[2],green[3]), file=additionals)
            
    with open("Data/trafficLight.add.xml", "a+") as additionals:
        print("</additional>\n",file=additionals)



def generate_routefile():
    #random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    with open("Data/Cross12.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
        guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="passenger"/>
        
        <route id="carflow1" edges="1NS1 1NS1_1" />
        <route id="carflow2" edges="1SN1 1SN1_1" />
        <route id="carflow3" edges="1WO1 1WO1_1" />
        <route id="carflow4" edges="1OW1 1OW1_1" />
        <route id="carflow5" edges="2NS1 2NS1_1" />
        <route id="carflow6" edges="2SN1 2SN1_1" />
        <route id="carflow7" edges="3NS1 3NS1_1" />
        <route id="carflow8" edges="3SN1 3SN1_1" />""", file=routes)
        vehNr = 0
        L = [0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]
        for i in range(N):
            for j in range(round(np.random.exponential(L[0]))):
                print('    <vehicle id="%i" type="typeWE" route="carflow1" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            for j in range(round(np.random.exponential(L[1]))):
                print('    <vehicle id="%i" type="typeWE" route="carflow2" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            for j in range(round(np.random.exponential(L[2]))):
                print('    <vehicle id="%i" type="typeNS" route="carflow3" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            for j in range(round(np.random.exponential(L[3]))):
                print('    <vehicle id="%i" type="typeNS" route="carflow4" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            for j in range(round(np.random.exponential(L[4]))):
                print('    <vehicle id="%i" type="typeNS" route="carflow5" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            for j in range(round(np.random.exponential(L[5]))):
                print('    <vehicle id="%i" type="typeNS" route="carflow6" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            for j in range(round(np.random.exponential(L[6]))):
                print('    <vehicle id="%i" type="typeNS" route="carflow7" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            for j in range(round(np.random.exponential(L[7]))):
                print('    <vehicle id="%i" type="typeNS" route="carflow8" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print("</routes>", file=routes)
             


# this is the main entry point of this script
if __name__ == "__main__":
    import time
    array =np.array([49,5,9,17])
    t = time.time()
    function_Cross_1_3(array)
    print("time for one function evaluation: ")
    print(time.time() - t)
    print(50*"=")
    print("optimisation")
    opt, fD = HC.hillClimbing(array, function_Cross_1_3, stepSize=1, functionEvaluation=24)
   