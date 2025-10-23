# Sets up the simulator

import Controller
import Globals
import numpy as np
import Objects
import random
from itertools import product

# initiate the setup process
# expects to receive the path to the data for setup, numNodes for network, and confirmation of the caseType (1 or 2).
def initiate(path, numNodes, caseType):

    if caseType == 1:
        buildRandom(numNodes)
    else:
        print("Component not ready yet")


# builds a network with a defined number of nodes
def buildRandom(numNodes):

    # poissan distribution of input numbers
    
    # avaerage number of inputs per node (mean K value)
    averageInput = Globals.averageInput
    
    # random nums approx between 0 and 4 if K=2
    inputNumArray = poissonReplaceZeros(averageInput, numNodes)


    # For loop to generate individual nodes
    for i in range (0, numNodes):
        newNode = Objects.Node()
        Globals.nodeDict[newNode.id] = newNode

    # For loop to assign input nodes randomly
    count = 0
    
    for nodeId, node in Globals.nodeDict.items():
        numInput = inputNumArray[count]
        for i in range (0, numInput):
            ranIn = random.choice(list(Globals.nodeDict.values()))
            while ranIn.id == nodeId or ranIn in node.inputNodes:
                ranIn = random.choice(list(Globals.nodeDict.values()))
            node.inputNodes.append(ranIn)
        count = count + 1

 
    # For loop to assign lookup tables
    for nodeId, node in Globals.nodeDict.items():

        tempDict = {}
        inputNodes = node.inputNodes
        numNodes = len(inputNodes)

        if numNodes > 0:
            # Generate combinations of zeros and ones
            combinations = list(product([0,1], repeat=numNodes))
            for array in combinations:
                lookupArray = array
                # In future this doesn't have to be random but for now it is
                output = random.randint(0, 1)
                node.lookupDict[lookupArray] = output


    Controller.mainMenu()

# Stops the distribution from having unconnected floating nodes  
def poissonReplaceZeros(lam, size):
    result = np.random.poisson(lam, size)
    while np.any(result == 0):
        zeros = (result == 0)
        result[zeros] = np.random.poisson(lam, np.sum(zeros))
    return result 
    
print("here")
