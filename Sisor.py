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

# introductory component to run a bulk degeneracy calc over 100 calc. Over x sisor timesteps.
def bulkSisor():
    # Preamble and initial option selection
    print("How many timesteps (each individually calculated)?")
    timesteps= input("Enter here: ")
    print("You said " + timesteps)
    timesteps = int(timesteps)

    count = 0
    started = False

    # resets everything
    Globals.tAveDegenDict = {}
    Globals.timestep = 0
    Globals.sisorDict = {}
    Globals.tAveDegenDict = {}

    # default timesteps to 1 (fixes issues)
    #timesteps = 1
    if timesteps >0:

        while count <= timesteps:
            
            timer = 0
            if len(Globals.tAveDegenDict) > 0:
                originalDict = Globals.sisorDict
                timer = Globals.timestep
            else:
                originalDict = Globals.nodeDict
                timer = Globals.timestep

            sisorDict = copy.deepcopy(originalDict)
            newSisorDict = runSisor(sisorDict, 1)
            # static num timesteps set to 20
            sisorDegeneracy = DegeneracySim.getDegeneracyMulti(newSisorDict, timer, 100)
            

                

            # sisor completed

            


            Globals.timestep = Globals.timestep + 1
            count = count + 1

                 

    else:
        print("timesteps must be greater than 0")
    
    print("Completed")

# introductory component
def sisorIntro(originalDict):
    # Preamble and initial option selection
    print("How many timesteps in a single calculation?")
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
       #origRedundancy = DegeneracySim.getRedundancy(Globals.nodeDict)
       
       print(f'Original Network Degeneracy: {origDegeneracy}')
       #print(f'Original Network Redundancy: {origRedundancy}')

       
       sisorDegeneracy = DegeneracySim.getDegeneracy(newSisorDict)
       #sisorRedundancy = DegeneracySim.getRedundancy(newSisorDict)

       print(f'SISOR Network Degeneracy: {sisorDegeneracy}')   
       #print(f'SISOR Network Redundancy: {sisorRedundancy}') 

       Globals.timestep = Globals.timestep + timesteps  

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
        node.removeLesion(nodeDict)
        node.resetStatus()
        node.bitFlipOnlyTimestep()
        node.sisorTimestep(frequency)
    
    # update status based on lookup tables
    for nodeId, node in nodeDict.items():
        node.updateStatus()
    
    workingDict = copy.deepcopy(nodeDict)

    # add SISOR algorithm component
    for nodeId, node in nodeDict.items():
        # The following is to replace what would happen in a C-CPSS at the real level
        # randomness normal distribution is used to determine node criticality
        #if node.status == 0:
        if node.sisorOutageFlag == True:
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
                # Set static
                #newChoice = 1
                if newChoice <= Globals.sisorNewNodeProb:
                    
                    currentNode = copy.deepcopy(node)
                    parentNodei = random.randint(0, len(node.inputNodes)-1)
                    parentNode = copy.deepcopy(node.inputNodes[parentNodei])

                    # find potential output nodes
                    
                    outputNodeList = []
                    for nodeIdentity, nodeItem in nodeDict.items():
                        for inNode in nodeItem.inputNodes:
                            if currentNode.id == inNode.id:
                                outputNodeList.append(nodeItem)
                        
                    # if there are output nodes, continue
                    testOutput = len(outputNodeList)
                    if testOutput > 0:
                     
                        # create new node
                        newNode = Objects.Node()
                        toAdd[newNode.id] = newNode
                        goAhead = True
                        chosenNode = newNode
                        chosenNodeId = newNode.id

                        # need to assign a child feeder
                        childNodeId = random.randint(0, len(outputNodeList)-1)
                        childNode =  copy.deepcopy(outputNodeList[childNodeId])
                    
                        while childNodeId == nodeId or childNode == node:
                            childNodeId = random.randint(1, len(nodeDict))
                            childNode =  copy.deepcopy(nodeDict[childNodeId])
                            
                    
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
                            childLookup = childNode.lookupDict

                            extLookup = {}
                            
                            for key, value in childLookup.items():
                                for newEntry in (0, 1):
                                    chance = random.random()
                                    # similarity percentage
                                    percentage = 0.25
                                    if chance < percentage:
                                        if value == 1:
                                            output = 0
                                        else:
                                            output = 1
                                        extLookup[key + (newEntry,)] = output
                                    else:
                                        output = value
                                        extLookup[key + (newEntry,)] = output
                                    
                            
                            childLookup = extLookup
                            childNode.lookupDict = childLookup 
                            
                            # changelog
                            workingDict[childNode.id] = childNode
                            Globals.changeLog.append(f'New Input Connection: {newNode.id} to {childNode.id}.')
                    
                    # OLDDDD

                    # parentNodei = random.randint(0, len(node.inputNodes)-1)
                    # parentNode = copy.deepcopy(node.inputNodes[parentNodei])

                    # # create new node
                    # newNode = Objects.Node()
                    # toAdd[newNode.id] = newNode
                    # goAhead = True
                    # chosenNode = newNode
                    # chosenNodeId = newNode.id

                    # # need to assign a child feeder
                    # childNodeId = random.randint(1, len(nodeDict))
                    # childNode =  copy.deepcopy(nodeDict[childNodeId])
                    
                    # while childNodeId == nodeId or childNode == node:
                    #     childNodeId = random.randint(1, len(nodeDict))
                    #     childNode =  copy.deepcopy(nodeDict[childNodeId])
                        
                    
                    # # make new lookup table for the new node
                    # tempDict = {}
                    # newNode.lookupDict = {}
                    # inputNodes = newNode.inputNodes
                    # inputNodes.append(parentNode)
                    # numNodes = len(inputNodes)

                    # if numNodes > 0:
                        
                    #     # Generate combinations of zeros and ones
                    #     combinations = list(product([0,1], repeat=numNodes))
                    #     for array in combinations:
                    #         lookupArray = array
                    #         # In future this doesn't have to be random but for now it is
                    #         output = random.randint(0, 1)
                    #         newNode.lookupDict[lookupArray] = output
                        
                    #     workingDict[newNode.id] = newNode
                    #     # add to changelog
                    #     Globals.changeLog.append(f'New Node: {newNode.id}.')
                    #     Globals.changeLog.append(f'New Input Connection: {parentNode.id} to {newNode.id}.')
                        

                    # # now connect to the receiver node (to replace broken node)
                    # childNode.lookupDict = {}
                    # childNode.inputNodes.append(newNode)
                    # targetNumNodes = len(childNode.inputNodes)
                    # if targetNumNodes > 0:
                    #     # Generate combinations of zeros and ones
                    #     combinations = list(product([0,1], repeat=targetNumNodes))
                    #     for array in combinations:
                    #         lookupArray = array
                    #         # In future this doesn't have to be random but for now it is
                    #         output = random.randint(0, 1)
                    #         childNode.lookupDict[lookupArray] = output
                    #     # changelog
                    #     workingDict[childNode.id] = childNode
                    #     Globals.changeLog.append(f'New Input Connection: {newNode.id} to {childNode.id}.')
                
                else:
                    # for the 0 node, add extra input node
                    currentNode = copy.deepcopy(node)
                    feederNodeList = currentNode.inputNodes

                    outputNodeList = []
                    for nodeIdentity, nodeItem in nodeDict.items():
                        for inNode in nodeItem.inputNodes:
                            if currentNode.id == inNode.id:
                                outputNodeList.append(nodeItem)
                    
                    
                    testFeeder = len(feederNodeList)
                    testOutput = len(outputNodeList)
                    if testFeeder > 0 and testOutput > 0:

                        count = 0
                        goAhead = True

                        for outNode in outputNodeList:
                            feederNodei = random.randint(0, len(feederNodeList)-1)
                            feederNode = copy.deepcopy(feederNodeList[feederNodei])

                            if feederNode == node or feederNode in outNode.inputNodes:
                                feederNodei = random.randint(0, len(feederNodeList)-1)
                                feederNode = copy.deepcopy(feederNodeList[feederNodei])
                                if count > 10:
                                    goAhead = False
                                    break

                            if goAhead == True:

                                outputNodeInputs = outNode.inputNodes
                                outputNodeInputs.append(feederNode)
                                outputLookup = outNode.lookupDict

                                numInputNodes = len(outputNodeInputs)

                                extLookup = {}
                                
                                for key, value in outputLookup.items():
                                    for newEntry in (0, 1):
                                        chance = random.random()
                                        # similarity percentage
                                        percentage = 0.25
                                        if chance < percentage:
                                            if value == 1:
                                                output = 0
                                            else:
                                                output = 1
                                        else:
                                            output = value
                                        extLookup[key + (newEntry,)] = output
                                
                                outputLookup = extLookup
                                outNode.lookupDict = outputLookup 
                                

                                # Add to changeLog
                                workingDict[outNode.id] = outNode
                                Globals.changeLog.append(f'New Input Connection: {feederNode.id} to {outNode.id}.')
                            
                    
                # REPEAT

                    #                 # for the 0 node, add extra input node
                    # currentNode = copy.deepcopy(node)

                    # feederNodei = random.randint(0, len(node.inputNodes)-1)
                    # feederNode = copy.deepcopy(node.inputNodes[feederNodei])

                    # outputNodes = []
                    # for nodeIdentity, nodeItem in nodeDict.items():
                    #     if node in nodeItem.inputNodes:
                    #         outputNodes.append(nodeItem)

                    # testChild = len(outputNodes)-1
                    #  # find child node (from outputs)
                    # if testChild >0:
                    #     childNodei = random.randint(0, len(outputNodes)-1)
                    #     childNode = copy.deepcopy(outputNodes[childNodei])
                    # else:

                    #     # find child node (ranmdom)
                    #     childNodei = random.randint(1, len(nodeDict))
                    #     childNode = copy.deepcopy(nodeDict[childNodei])

                    # count = 0
                    # goAhead = True

                    # while currentNode.id == childNode.id or  feederNode in childNode.inputNodes or feederNode == childNode:
                    #     if testChild >0:
                    #         childNodei = random.randint(0, len(outputNodes)-1)
                    #         childNode = copy.deepcopy(outputNodes[childNodei])
                    #     else:

                    #         # find child node (ranmdom)
                    #         childNodei = random.randint(1, len(nodeDict))
                    #         childNode = copy.deepcopy(nodeDict[childNodei])
                    #     count = count+1
                    #     if count > 10:
                    #         goAhead = False
                    #         break

                    # if goAhead == True:

                        
                    #     childNodeInputs = childNode.inputNodes
                    #     childNodeInputs.append(feederNode)
                        
                    #     numNodes = len(childNodeInputs)

                    #     if numNodes > 0:
                    #         # make new lookup table
                    #         childNode.lookupDict = {}
                            
                    #         # Generate combinations of zeros and ones
                    #         combinations = list(product([0,1], repeat=numNodes))
                    #         for array in combinations:
                    #             lookupArray = array
                    #             # In future this doesn't have to be random but for now it is
                    #             output = random.randint(0, 1)
                    #             childNode.lookupDict[lookupArray] = output

                    #         # Add to changeLog
                    #         workingDict[childNode.id] = childNode
                    #         Globals.changeLog.append(f'New Input Connection: {feederNode.id} to {childNode.id}.')
                        
                
                #     #     # table updated!
        
        
    # add any new nodes to the updated dict
    if len(toAdd) > 0:
        for key, value in toAdd.items():
            workingDict[key] = value
    
            
    nodeDict = workingDict
    return nodeDict


# def calcMINewLink(startNode, middleNode, EndNode):
     
#     combinedDict = {}

#     # reference to the start node in the middleNode inputNode lsit
#     middleRef = None
    
#     counter = 0
#     for inNode in middleNode.inputNodes:
#         if inNode == startNode:
#             middleRef = counter
#         counter = counter + 1
    
#     for entry, output in middleNode.lookupDict.items():
#         entryArray = entry.split(",")
#         middleRef



#     input = 0
#     output = 0
#     return input, output