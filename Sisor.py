# algorithm to apply the SISOR methodology to a given ystem

import Globals
import math
import numpy as np
from scipy.stats import norm
import random
from itertools import product
import DegeneracySim
import copy
import Objects

# introductory component
def sisorIntro(originalDict):
    # Preamble and initial option selection
    print("How many timesteps?")
    timesteps= input("Enter here: ")
    print("You said " + timesteps)
    timesteps = int(timesteps)

    # default timesteps to 1 (fixes issues)
    #timesteps = 1
    if timesteps >0:


       # sisor completed

       sisorDict = copy.deepcopy(originalDict)
       newSisorDict = runSisor(sisorDict, timesteps)
       
       origDegeneracy = DegeneracySim.getDegeneracy(Globals.nodeDict)
       
       print(f'Original Network Degeneracy: {origDegeneracy}')

       
       sisorDegeneracy = DegeneracySim.getDegeneracy(newSisorDict)

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
            nodeDict = doSisor(nodeDict, frequency)
            # close off sisor
            if step == numTimesteps+1:
                for nodeId, node in nodeDict:
                    node.sisorFinish()
    print("")
    Globals.sisorDict = nodeDict
    return(nodeDict)
            




# does the Sisor algorithm
def doSisor(nodeDict, frequency ):
    toAdd = {}
    newDict = {}
    newDictTwo = {}
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
    
    workingDict = copy.deepcopy(nodeDict)

    # add SISOR algorithm component
    for nodeId, node in nodeDict.items():
        # The following is to replace what would happen in a C-CPSS at the real level
        # randomness normal distribution is used to determine node criticality
        if node.status == 0:
            mean = 0.50
            sD = 0.15
            currentCriticality = np.random.normal(loc=mean, scale=sD)
            currentCriticality = max(0, min(1, currentCriticality))
            # criticality determines likelihood of new sisor outcome to occur being generated
            # assume one for one for now
            chance = random.random()
            # if new connection/node to occur
            if chance < currentCriticality:
                
                # determine if its a new node or new connection
                newChoice = random.random()
                if newChoice <= Globals.sisorNewNodeProb:
                    # If creating a new node
                    # select a random input node from inputnode list
                    parentNodei = random.randint(0, len(node.inputNodes)-1)
                    parentNode = node.inputNodes[parentNodei]

                    # create new node
                    newNode = Objects.Node()
                    toAdd[newNode.id] = newNode
                    goAhead = True
                    chosenNode = newNode
                    chosenNodeId = newNode.id

                    # need to assign a child feeder
                    childNodeId = random.randint(1, len(nodeDict))
                    childNode =  nodeDict[childNodeId]
                    
                    while childNodeId == nodeId or childNode == node:
                        childNodeId = random.randint(1, len(nodeDict))
                        childNode =  nodeDict[childNodeId]
                        
                    
                    # make new lookup table for the new node
                    tempDict = {}
                    newNode.lookupDict = {}
                    inputNodes = newNode.inputNodes
                    inputNodes.append(parentNode)
                    numNodes = len(inputNodes)

                    if numNodes > 0:
                        
                        # Generate combinations of zeros and ones
                        combinations = list(product([0,1], repeat=numNodes))
                        for array in combinations:
                            lookupArray = array
                            # In future this doesn't have to be random but for now it is
                            output = random.randint(0, 1)
                            newNode.lookupDict[lookupArray] = output
                        
                        workingDict[newNode.id] = newNode
                        # add to changelog
                        Globals.changeLog.append(f'New Node: {newNode.id}.')
                        Globals.changeLog.append(f'New Input Connection: {parentNode.id} to {newNode.id}.')
                        

                    # now connect to the receiver node (to replace broken node)
                    
                    childNode.inputNodes.append(newNode)
                    targetNumNodes = len(childNode.inputNodes)
                    if targetNumNodes > 0:
                        # Generate combinations of zeros and ones
                        combinations = list(product([0,1], repeat=targetNumNodes))
                        for array in combinations:
                            lookupArray = array
                            # In future this doesn't have to be random but for now it is
                            output = random.randint(0, 1)
                            childNode.lookupDict[lookupArray] = output
                        # changelog
                        workingDict[childNode.id] = childNode
                        Globals.changeLog.append(f'New Input Connection: {newNode.id} to {childNode.id}.')
                
                else:

                    # Else create a new connection
                    inputNodei = random.randint(0, len(node.inputNodes)-1)
                    inputNode = node.inputNodes[inputNodei]

                    chosenNodeId = random.randint(1, len(nodeDict))
                    chosenNode = nodeDict[chosenNodeId]
                    count = 0
                    goAhead = True

                    while chosenNodeId == inputNode.id or chosenNode in inputNode.inputNodes:
                        chosenNodeId = random.randint(1, len(nodeDict))
                        chosenNode =  nodeDict[chosenNodeId]
                        count = count+1
                        if count > 10:
                            goAhead = False
                            break

                    if goAhead == True:

                        # make new lookup table
                        tempDict = {}
                        inputNode.lookupDict = {}
                        chosenNodeInputs = chosenNode.inputNodes
                        chosenNodeInputs.append(inputNode)
                        numNodes = len(chosenNodeInputs)

                        if numNodes > 0:
                            # Generate combinations of zeros and ones
                            combinations = list(product([0,1], repeat=numNodes))
                            for array in combinations:
                                lookupArray = array
                                # In future this doesn't have to be random but for now it is
                                output = random.randint(0, 1)
                                chosenNode.lookupDict[lookupArray] = output

                            # Add to changeLog
                            workingDict[chosenNode.id] = chosenNode
                            Globals.changeLog.append(f'New Input Connection: {inputNode.id} to {chosenNode.id}.')
                            
                        # table updated!
        
        
    # add any new nodes to the updated dict
    if len(toAdd) > 0:
        for key, value in toAdd.items():
            workingDict[key] = value
    
            
    nodeDict = workingDict
    return nodeDict