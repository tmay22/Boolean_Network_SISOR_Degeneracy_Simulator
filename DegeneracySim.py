# Simulation functions for Degeneracy
import Globals
import math
from collections import Counter
from itertools import product
import itertools
import Graph
from datetime import datetime
import csv
import copy
import Export


def getDegenMultiTSteps(inputNodeDictOrig, timeIn):

    # find out how many count
    # Preamble and initial option selection
    print("How many timesteps?")
    timesteps= input("Enter here: ")
    print("You said " + timesteps)
    timesteps = int(timesteps)

    getDegeneracyMulti(inputNodeDictOrig, timeIn, timesteps)


# run multiple degeneracy calculations
def getDegeneracyMulti(inputNodeDictOrig, timeIn, timesteps):

    inputNodeDict = copy.deepcopy(inputNodeDictOrig)

    

    details = f'{Globals.sessionId}_T{timeIn}_K{Globals.averageInput}.N{Globals.numNodes}.P{int(Globals.sisorNewNodeProb*100)}'

    outDict = {}
    aveMIGraphDict = {}
    aveScalarSysMIGraphDict = {}
    aveDegenDict = {}

    uMIDict = {}
    uScalarDict = {}
    uDegenDict = {}


    

    count = 0

    if timesteps > 0:

        

        while count < timesteps:
            
           
                # N val
            numNodes = len(inputNodeDict)
            # X val
            nodeList = []
            # K val
            averageInput = Globals.averageInput

            for name,value in inputNodeDict.items():
                nodeList.append(value)

            


            # Get the system's Mutual information
            mI = getSystemMI(inputNodeDict)
            aveMIDict = {}
            allresultDict = {}
            aveResultDict = {}
            wholeSubResultDict = {}
            sumTotal = 0
            # start the sum component
            print("...Calculating Sum Components...")
            for u in range (1, numNodes+1):
                print(f'...{u}/{numNodes}...')
                aveMI = getAveMI(u, inputNodeDict)
                aveMIDict[u] = aveMI
                scalar = u/numNodes

                
                partA = aveMI
                partB = scalar * mI

                equation = partA - partB
                allresultDict[u] = equation
                aveResultDict[u] = partA
                wholeSubResultDict[u] = partB
                sumTotal = sumTotal + equation

                if u in uMIDict:
                    array = uMIDict[u]
                    array.append(partA)
                else:
                    uMIDict[u] = [partA]

                if u in uScalarDict:
                    array = uScalarDict[u]
                    array.append(partB)
                else:
                    uScalarDict[u] = [partB]

                if u in uDegenDict:
                    array = uDegenDict[u]
                    array.append(equation)
                else:
                    uDegenDict[u] = [equation]
                

                #print(f'{u} size complete.')

            print(f'\n')
            print(f'Degeneracy Calculation Completed')
            print(f'DN(x;O) = {sumTotal}')
            cleanup(inputNodeDict)
            #Graph.plotDegeneracyEq(aveResultDict,wholeSubResultDict)
            #Graph.plotDegeneracyOnly(allresultDict)
            #
            # eturn sumTotal
            outDict[count] = sumTotal



            count = count + 1

    path = "./Individual_Sim_Outputs"
    details = str(details)
    file = str(f'{path}/{details}.csv')

    Export.expNewDict(file,outDict)

    # with open(file, 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['Key', 'Value'])  # header
    #     for key, value in outDict.items():
    #         writer.writerow([key, value])

    posCount = 0
    posSum = 0
    allSum = 0
    for id, val in outDict.items():
        allSum = allSum + val
        if val > 0:
            posSum = posSum + val
            posCount = posCount + 1
    
    allAve = allSum / timesteps
    posAve = posSum / posCount

    aveSum = 0
    aveScalar = 0
    aveDegen = 0

    for uVal, arrayAns in uMIDict.items():
        for num in arrayAns:
            aveSum = aveSum + num
        calc = aveSum / len(arrayAns)
        aveMIGraphDict[uVal] = calc
    
    for uVal, arrayAns in uScalarDict.items():
        for num in arrayAns:
            aveScalar = aveScalar + num
        calc = aveScalar / len(arrayAns)
        aveScalarSysMIGraphDict[uVal] = calc

    for uVal, arrayAns in uDegenDict.items():
        for num in arrayAns:
            aveDegen = aveDegen + num
        calc = aveDegen / len(arrayAns)
        aveDegenDict[uVal] = calc


    print(f'----------------------------------------')

    print(f'Average of all degeneracies for {file}:\n {allAve}')
    #print(f'Average of positive-only degeneracies for {file}:\n {posAve}')

    # TURN GRAPHS ON AND OFF FOR CONVENIENCE HERE
    #Graph.plotDegeneracyEq(aveMIGraphDict,aveScalarSysMIGraphDict)
    #Graph.plotDegeneracyOnly(aveDegenDict)

    # Add to global tracking for average degeneracy
    Globals.tAveDegenDict[timeIn] = allAve

    print(f'----------------------------------------')

# get the redundancy of the system
def getRedundancy(nodeDict):
    redCalc = 0
    redSum = 0
    redDict = {}
    partADict = {}
    partBDict = {}

    numSubsets = len(nodeDict.items())

    partB = getSystemMI(nodeDict)

    for i in range (1, numSubsets+1):

        selectNode = nodeDict[i]
        tempDict = {}
        tempDict[1] = selectNode
        
        print(f'...{i}/{numSubsets}...')
        partA = getSystemMI(tempDict)

        
        redSum = redSum + partA
        
        partADict[i] = partA
    
    redCalc = redSum - partB

    
    #Graph.plotRedundancy(partADict,partBDict)
    #Graph.plotRedundancyOnly(redDict)
    return redCalc



# get the degeneracy of system
def getDegeneracy(inputNodeDictOrig):

    inputNodeDict = copy.deepcopy(inputNodeDictOrig)

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
    mI = getSystemMI(inputNodeDict)
    aveMIDict = {}
    allresultDict = {}
    aveResultDict = {}
    wholeSubResultDict = {}
    sumTotal = 0
    # start the sum component
    print("...Calculating Sum Components...")
    for u in range (1, numNodes+1):
        print(f'...{u}/{numNodes}...')
        aveMI = getAveMI(u, inputNodeDict)
        aveMIDict[u] = aveMI
        scalar = u/numNodes

        
        partA = aveMI
        partB = scalar * mI

        equation = partA - partB
        allresultDict[u] = equation
        aveResultDict[u] = partA
        wholeSubResultDict[u] = partB
        sumTotal = sumTotal + equation

        #print(f'{u} size complete.')

    print(f'\n')
    print('System MI:', mI)
    print('Subset Sizes:', u)
    print('Ave MI per subset:', aveMIDict)
    print('Scaled System MI:', [u/numNodes * mI for u in range(1,numNodes+1)])
    print(f'Degeneracy Calculation Completed')
    print(f'DN(x;O) = {sumTotal}')
    cleanup(inputNodeDict)
    Graph.plotDegeneracyEq(aveResultDict,wholeSubResultDict)
    Graph.plotDegeneracyOnly(allresultDict)
    return sumTotal
    print(f'\n')


    # want something to graph this too - STRETCH


# def get average mutual information during pertubation
def getAveMI(subsetSize, inputNodeDict):
    
    u = subsetSize
    nodeIds = list(inputNodeDict.keys())

    # Generate subsets
    subsets = list(itertools.combinations(nodeIds, u))

    jMiArray = []

    for subsetJ in subsets:
        # get node Obj
        jNodeList = {}
        for jid in subsetJ:
            nvalue = inputNodeDict[jid]
            jNodeList[jid] = nvalue
        
        # get subset mutual information under pertubation
        jMi = getSubSystemMI(jNodeList)
        jMiArray.append(jMi)
        #print(f'Size {u} Subset {subsetJ} MI {jMi}')
    
    average = sum(jMiArray) / len(jMiArray)
    #print(f'\n{subsetSize} Calculation Complete. Average: {average}')
    #print("here")

    return average

def getEntropy(probabilityDistributionList):
    #Calculate entropy from probability distribution list
    res = -sum(p * math.log2(p) for p in probabilityDistributionList if p > 0)
    return res 

# Get mutual information of sub system
def getSubSystemMI(nodeList):

    #print("...Calculating Sub-System Mutual Information...")

    # add pertubation and lesioning
    for nodeId, node in nodeList.items():
        node.timestep()
        node.lesionTimestep(nodeList)

    # update status based on lookup tables
    for nodeId, node in nodeList.items():
        node.updateStatus()
        
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
    #print(f'Sub-System Mutual Information: {mutualInformation_system}')
    
    # Finish lesioning
    for nodeId, node in nodeList.items():
        node.removeLesion(nodeList)

    return mutualInformation_system
    print("here")



# Get mutual information of entire system
def getSystemMI(nodeList):

    print("...Calculating System Mutual Information...")

    # add pertubation
    for nodeId, node in nodeList.items():
        node.timestep()
        node.lesionTimestep(nodeList)

    # update status based on lookup tables
    for nodeId, node in nodeList.items():
        node.updateStatus()
        
    # get a list of all the input states

    allInputStates = [list(node.lookupDict.keys()) for node in nodeList.values()]
    
    #All the nodes tables times by each other
    productInputStates = list(product(*allInputStates))
    
    combinedInputs = []
    combinedOutputs = []

    for productInputOption in productInputStates:
        temp_combinedTotalInput = []
        temp_combinedTotalOutput = []
        # Iterate directly over node objects, matching input arrays in order
        for node, inputArray in zip(nodeList.values(), productInputOption):
            # add to flat combinedTotalInput list
            temp_combinedTotalInput.extend(inputArray)
            # get output value for that input node combination
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
    #print(f'System Mutual Information: {mutualInformation_system}')

    # Finish lesioning
    for nodeId, node in nodeList.items():
        node.removeLesion(nodeList)

    return mutualInformation_system
    #print("here")




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

# cleanup lesions at the end
def cleanup(nodeDict):
    for nodei, node in nodeDict.items():
        node.removeLesion(nodeDict)