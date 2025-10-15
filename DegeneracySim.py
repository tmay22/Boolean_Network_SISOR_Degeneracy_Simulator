# Simulation functions for Degeneracy
import Globals
import math
from collections import Counter


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

    # start the sum component
    for u in range (1, numNodes+1):
        aveMI = getAveMI()
        scalar = u/numNodes
        mI = getMI()





    # want something to graph this too - STRETCH

# def get average mutual information during pertubation
def getAveMI():
    return None

def getEntropy(probabilityDistributionList):
    #Calculate entropy from probability distribution list
    res = -sum(p * math.log2(p) for p in probabilityDistributionList if p > 0)
    return res 

# get the mutual information during pertubation
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