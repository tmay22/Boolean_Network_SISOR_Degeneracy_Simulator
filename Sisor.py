# algorithm to apply the SISOR methodology to a given ystem

import Globals
import math
import numpy as np
from scipy.stats import norm
import random
from itertools import product
import DegeneracySim
import copy

# introductory component
def sisorIntro(originalDict):
    # Preamble and initial option selection
    print("How many timesteps?")
    timesteps= input("Enter here: ")
    print("You said " + timesteps)
    timesteps = int(timesteps)

    if timesteps >0:


       # sisor completed

       sisorDict = copy.deepcopy(originalDict)
       sisorDict = runSisor(sisorDict, timesteps)
       
       origDegeneracy = DegeneracySim.getDegeneracy(Globals.nodeDict)
       
       print(f'Original Network Degeneracy: {origDegeneracy}')

       
       sisorDegeneracy = DegeneracySim.getDegeneracy(sisorDict)

       print(f'SISOR Network Degeneracy: {sisorDegeneracy}')   

       print("COMPLETED")     

    else:
        print("timesteps must be greater than 0")


# runs an iteration of the SISOR logic against the chosen RBN
# Note that because this is an RBN the new connections made are also 'random' - 
def runSisor(nodeDict, numTimesteps):

    # Calculate SISOR frequency
    conflictDP = Globals.sisorConflictDp
    sensConflict = Globals.sisorSensConflict
    maxDeg = Globals.sisorMaxDegradation
    conflictLikelihood = Globals.sisorConflictProb

    frequency = 0

    if 0 <= conflictLikelihood < conflictDP:
        frequency = maxDeg / (1 + math.exp(-sensConflict * (conflictLikelihood-(conflictDP/2))) +1)
    elif conflictDP <= 0 <= 1:
        frequency = maxDeg * ((1-conflictLikelihood)/(1-conflictDP))
    else:
        print("conflict likelihood input error")
    
    # Loop through timesteps
    if frequency != 0:
        print("...Starting SISOR Replication...")
        for step in range(1, numTimesteps+1):
            print(f'...Timestep {step}/{numTimesteps}...')
            
            # add chance of random bitflip
            # add sisor outages
            # resets the past status of all nodes
            for nodeId, node in nodeDict.items():
                node.resetStatus()
                node.bitFlipOnlyTimestep()
                node.sisorTimestep(frequency)
            
            # update status based on lookup tables
            for nodeId, node in nodeDict.items():
                inputNodes = node.inputNodes
                lookupTable = node.lookupDict
                resultArray = []
                # looks up the PAST status of the nodes in the input node list (in case they have already updated)
                for node in inputNodes:
                    nodeStatus = node.pastStatus
                    resultArray.append(nodeStatus)
                # convert array to tuple
                resultTuple = tuple(resultArray)

                # Lookup new status and update
                lookupStatus = lookupTable[resultTuple]
                node.status = lookupStatus
            
            # add SISOR algorithm component
            for nodeId, node in nodeDict.items():
                # The following is to replace what would happen in a C-CPSS at the real level
                # randomness normal distribution is used to determine node criticality
                if node.status == 0:
                    mean = 0.50
                    sD = 0.15
                    currentCriticality = np.random.normal(loc=mean, scale=sD)
                    currentCriticality = max(0, min(1, currentCriticality))
                    # criticality determines likelihood of new connection being generated
                    # assume one for one for now
                    chance = random.random()
                    # if new connection to occur
                    if chance < currentCriticality:
                        chosenNodeId = random.randint(1, len(nodeDict))
                        chosenNode = nodeDict[chosenNodeId]
                        count = 0
                        goAhead = True
                        while chosenNodeId == nodeId or chosenNode in node.inputNodes:
                            chosenNodeId = random.randint(1, len(nodeDict))
                            chosenNode =  nodeDict[chosenNodeId]
                            count = count+1
                            if count > 10:
                                goAhead = False
                                break

                        if goAhead == True:
                            # Backups just in case
                            oldInputNodes = node.inputNodes.copy()
                            oldlookupDict = node.lookupDict.copy()

                            # make new lookup table
                            tempDict = {}
                            node.lookupDict = {}
                            inputNodes = node.inputNodes
                            inputNodes.append(chosenNode)
                            numNodes = len(inputNodes)

                            if numNodes > 0:
                                # Generate combinations of zeros and ones
                                combinations = list(product([0,1], repeat=numNodes))
                                for array in combinations:
                                    lookupArray = array
                                    # In future this doesn't have to be random but for now it is
                                    output = random.randint(0, 1)
                                    node.lookupDict[lookupArray] = output

                            # table updated!
                if step == numTimesteps+1:
                    node.sisorFinish()

    print("")
    Globals.sisorDict = nodeDict
    return(nodeDict)
            





        