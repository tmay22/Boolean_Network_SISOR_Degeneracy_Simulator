# Simulation functions for Degeneracy
import Globals
import math
from collections import Counter
from itertools import product
import itertools


# get the degeneracy of system
def getDegeneracy(inputNodeDict):

    # N val
    numNodes = len(inputNodeDict)
    # X val
    nodeList = []
    # K val
    averageInput = Globals.averageInput

    for name,value in inputNodeDict.items():
        nodeList.append(value)

    # SOMETHING IS WRONG WITH THE GRAPHS
    # dictionary of the key value pairs of the degeneracy graph (x,y)
    graphD = {}
    # dictionary of the key value pairs of the MI graph (x,y)
    graphMI = {}


    # Get the system's Mutual information
    mI = getSystemMI(Globals.nodeDict)
    aveMIDict = {}
    resultDict = {}
    sumTotal = 0
    # start the sum component
    for u in range (1, numNodes+1):
        aveMI = getAveMI(u)
        aveMIDict[u] = aveMI
        scalar = u/numNodes

        partA = aveMI
        partB = scalar * mI

        equation = partA - partB
        resultDict[u] = equation
        sumTotal = sumTotal + equation

        print(f'{u} size complete.')

    print(f'Degeneracy Calculation Completed')
    print(f'DN(x;O) = {sumTotal}')
    print(f'\n')


    # want something to graph this too - STRETCH


# def get average mutual information during pertubation
def getAveMI(subsetSize):
    
    u = subsetSize
    nodeIds = list(Globals.nodeDict.keys())

    # Generate subsets
    subsets = list(itertools.combinations(nodeIds, u))

    jMiArray = []

    for subsetJ in subsets:
        # get node Obj
        jNodeList = {}
        for jid in subsetJ:
            nvalue = Globals.nodeDict[jid]
            jNodeList[jid] = nvalue
        
        # get subset mutual information under pertubation
        jMi = getSubSystemMI(jNodeList)
        jMiArray.append(jMi)
        print(f'Size {u} Subset {subsetJ} MI {jMi}')
    
    average = sum(jMiArray) / len(jMiArray)
    print(f'\n{subsetSize} Calculation Complete. Average: {average}')
    print("here")

    return average

def getEntropy(probabilityDistributionList):
    #Calculate entropy from probability distribution list
    res = -sum(p * math.log2(p) for p in probabilityDistributionList if p > 0)
    return res 

# Get mutual information of sub system
def getSubSystemMI(nodeList):

    print("...Calculating Sub-System Mutual Information...")

    # add pertubation
    for nodeId, node in nodeList.items():
        node.timestep()


    # get a list of all the input states

    allInputStates = [list(node.lookupDict.keys()) for node in nodeList.values()]
    
    #All the nodes tables times by each other
    productInputStates = list(product(*allInputStates))
    
    combinedInputs = []
    combinedOutputs = []

    for productInputOption in productInputStates:
        temp_combinedTotalInput = []
        temp_combinedTotalOutput = []

        for node, inputArray in zip(nodeList.values(), productInputOption):
            temp_combinedTotalInput.extend(inputArray)
            outputVal = node.lookupDict[inputArray]
            temp_combinedTotalOutput.append(outputVal)

        # Add to overall inputs and outputs
        combinedInputs.append(tuple(temp_combinedTotalInput))
        combinedOutputs.append(tuple(temp_combinedTotalOutput))
        
        #print("here")

    # compute probability distributions

    # inputs
    countInputs = Counter(combinedInputs)
    sumInputs = sum(countInputs.values())
    # Input probability distribution
    probDistInput = [count / sumInputs for count in countInputs.values()]
    # Input entropy
    entropyInput_X = getEntropy(probDistInput)

    # outputs
    countOutputs = Counter(combinedOutputs)
    sumOutputs = sum(countOutputs.values())
    # Output probability distribution
    probDistOutput = [count / sumOutputs for count in countOutputs.values()]
    # Output entropy
    entropyOutput_O = getEntropy(probDistOutput)

    # joint input output
    countJoint = Counter(zip(combinedInputs, combinedOutputs))
    sumJoint = sum(countJoint.values())
    # Joint probability distribution list
    probDistJoint = [count / sumJoint for count in countJoint.values()]
    # joint entropy
    entropyJoint_XO = getEntropy(probDistJoint)


    # Calculate MI of whole system
    mutualInformation_system = entropyInput_X + entropyOutput_O - entropyJoint_XO
    print(f'Sub-System Mutual Information: {mutualInformation_system}')
    return mutualInformation_system
    print("here")



# Get mutual information of entire system
def getSystemMI(nodeList):

    print("...Calculating System Mutual Information...")

    # add pertubation
    for nodeId, node in nodeList.items():
        node.timestep()


    # get a list of all the input states

    allInputStates = [list(node.lookupDict.keys()) for node in nodeList.values()]
    
    #All the nodes tables times by each other
    productInputStates = list(product(*allInputStates))
    
    combinedInputs = []
    combinedOutputs = []

    for productInputOption in productInputStates:
        temp_combinedTotalInput = []
        temp_combinedTotalOutput = []
        for nodeCount, inputArray in enumerate(productInputOption):
            # add to flat combinedTotalInput list
            temp_combinedTotalInput.extend(inputArray)
            # get current node from globals
            currentNode = Globals.nodeDict[nodeCount+1]
            # get output value for that input node combination
            outputVal = currentNode.lookupDict[inputArray]
            temp_combinedTotalOutput.append(outputVal)
        # Add to overall inputs and outputs
        combinedInputs.append(tuple(temp_combinedTotalInput))
        combinedOutputs.append(tuple(temp_combinedTotalOutput))
        
        #print("here")

    # compute probability distributions

    # inputs
    countInputs = Counter(combinedInputs)
    sumInputs = sum(countInputs.values())
    # Input probability distribution
    probDistInput = [count / sumInputs for count in countInputs.values()]
    # Input entropy
    entropyInput_X = getEntropy(probDistInput)

    # outputs
    countOutputs = Counter(combinedOutputs)
    sumOutputs = sum(countOutputs.values())
    # Output probability distribution
    probDistOutput = [count / sumOutputs for count in countOutputs.values()]
    # Output entropy
    entropyOutput_O = getEntropy(probDistOutput)

    # joint input output
    countJoint = Counter(zip(combinedInputs, combinedOutputs))
    sumJoint = sum(countJoint.values())
    # Joint probability distribution list
    probDistJoint = [count / sumJoint for count in countJoint.values()]
    # joint entropy
    entropyJoint_XO = getEntropy(probDistJoint)


    # Calculate MI of whole system
    mutualInformation_system = entropyInput_X + entropyOutput_O - entropyJoint_XO
    print(f'System Mutual Information: {mutualInformation_system}')
    return mutualInformation_system
    print("here")




# OLDDDDDDD gets it only for a single node with no pertubation
def getMI(nodeList):

    for node in nodeList:
        # find out probability of each combination
        stateOptions = node.lookupDict.len()
        combinationProb = 1/stateOptions

        # standard for binary to be approximately 50%
        #   Calculate the marginal probability for output values (0 or 1)
        outVal = list(node.lookupDict.values())
        outCount = Counter(outVal)
        totalOutputs = len(outVal)
        
        # Probability distribution of outputs p(o)
        outputProbDist = []
        for count in outCount.values():
            res = count / totalOutputs
            outputProbDist.append(res)
        
        # Output Entropy
        entropy_Oval = getEntropy(outputProbDist)
        
        # compute inpute probability
        inputProbDist = combinationProb * stateOptions

        # Input Entropy
        entropy_Xval = getEntropy(inputProbDist)

        # joint distribution probability of X and O
        jointList = list(node.lookupDict.items())
        jointCounts = Counter(jointList)
        totalJoint = jointList.len()

        # get joint probability distribution
        jointProbDist = []
        for count in jointCounts.values():
            res = count / totalJoint
            jointProbDist.append(res)
        
        # joint entropy value
        entropy_XOval = getEntropy(jointProbDist)

        # unique pairs is n to power of num inputs
        uniquePairs = pow(2,stateOptions)
        uniqueProb = 1/uniquePairs # (X)

        # mutual Information calculation
        mutualInformation = entropy_Xval + entropy_Oval - entropy_XOval


    return None