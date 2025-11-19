# Contains the object classes
import uuid
import random
import Globals
import copy

# Represents a Node in the network
class Node:

    def __init__(self):
        Globals.indexCounter = Globals.indexCounter + 1
        self.id = Globals.indexCounter
        # inputNodes is expected to be a list of Nodes
        self.inputNodes = []
        # lookup output table
        self.lookupDict = {}
        self.domain = None
        if Globals.caseType == 1:
            self.randDomain()
        # Set status to 1 by default
        self.status = 1
        # Past status as per previous timestamp
        self.pastStatus = 1
        # A flag to recognise outage is because of SISOR not other event
        self.sisorOutageFlag = False
        # A flag to recongise if the node has been lesioned (outward connections cut)
        self.lesionFlagSource = False
        # A flag to identify a node that has been affected by lesioning (inward connections cut)
        self.lesionFlagChild = False
        # the saved lookup dictionary pre-lesion
        self.savedLookupDict = {}
        # the saved input nodes pre-lesion
        self.savedInputNodes = []

    # removes any lesions from the code
    def removeLesion(self, nodeDict):
        # reset if already experiencing lesion as source
        if self.lesionFlagSource == True:
            self.lesionFlagSource = False
            # get list of child nodes
            # outputNodeList = []
            # for nodeIdentity, nodeItem in nodeDict.items():
            #     for inNode in nodeItem.inputNodes:
            #         if self.id == inNode.id:
            #             outputNodeList.append(nodeItem)
                
            # # if there are child output nodes, continue
            # testOutput = len(outputNodeList)
            # if testOutput > 0:
            #     for childNode in outputNodeList:
            #         childNode.resetLesionChild()


        

            
        # reset if already experiencing lesion as  child
        if self.lesionFlagChild == True:
                self.lookupDict = copy.deepcopy(self.savedLookupDict)
                self.inputNodes = copy.deepcopy(self.savedInputNodes)
                self.lesionFlagChild = False
            

    # lesion the node
    def lesionTimestep(self, nodeDict):
        
        self.removeLesion(nodeDict)


        # CREATE NEW LESIONS IF NEEDED
        lesionProb = Globals.lesion
        res = random.random()
        if res<lesionProb:
            
            # get list of child nodes
            outputNodeList = []
            for nodeIdentity, nodeItem in nodeDict.items():
                for inNode in nodeItem.inputNodes:
                    if self.id == inNode.id:
                        outputNodeList.append(nodeItem)
                
            # if there are child output nodes, continue
            testOutput = len(outputNodeList)

            if testOutput > 0:   
                # run lesionCommand on child nodes
                for outNode in outputNodeList:
                    outNode.lesionCommand(self)
                self.lesionFlagSource = True


    # receive a command to lesion
    def lesionCommand(self, parentNode):
        # get index of parentNode
        index = -1
        count = 0
        for inNode in self.inputNodes:
            if inNode.id == parentNode.id:
                index = copy.deepcopy(count)
            count = count + 1
        # if found
        zeroCounterDict  = {}
        oneCounterDict = {}
        counterDict = {}
        finalDict = {}
        if index >= 0:
            self.savedInputNodes = copy.deepcopy(self.inputNodes)
            del self.inputNodes[index]
            for inputTuple, output in self.lookupDict.items():
                updatedTuple = inputTuple[:index] + inputTuple[index+1:]
                if len(updatedTuple) > 0:
                    # see whether it got more zeros or ones
                    if output == 0:
                        if updatedTuple in zeroCounterDict:
                            oldCount = zeroCounterDict[updatedTuple]
                            newCount = oldCount + 1
                        else:
                            zeroCounterDict[updatedTuple] = 1
                    if output == 1:
                        if updatedTuple in oneCounterDict:
                            oldCount = oneCounterDict[updatedTuple]
                            newCount = oldCount + 1
                        else:
                            oneCounterDict[updatedTuple] = 1
            
            if len(zeroCounterDict) > 0:
                
                # make final dict for lesioning 
                for zeroKey, zeroCount in zeroCounterDict.items():
                    finalDict[zeroKey] = 0
            
            if len(oneCounterDict) > 0:

                for oneKey, oneValue in oneCounterDict.items():
                    if oneKey in finalDict:
                        zeroVal = zeroCounterDict[oneKey]
                        
                        if zeroVal > oneValue:
                            highest = 0
                        elif zeroVal == oneValue:
                            res = random.randint(0,1)
                            highest = res
                        else:
                            highest = 1
                        finalDict[oneKey] = highest
                    else:
                        finalDict[oneKey] = 1
            
            self.savedLookupDict = copy.deepcopy(self.lookupDict)
            self.lookupDict = finalDict
            self.lesionFlagChild = True
            

                        




    
    # Assign a random domain to the node
    def randDomain(self):
        # Determine domain
        numbers = [1, 2, 3]
        no = random.choice(numbers)
        if no == 1:
            self.domain = "Cyber"
        elif no == 2:
            self.domain = "Physical"
        elif no == 3:
            self.domain = "Social"
    
    # pertubates and bitflips node
    def timestep(self):
        bitFlipProb = Globals.ranBitFlip
        pertubationProb = Globals.pertubation

        flip = False
        res = random.random()
        if res <= bitFlipProb:
            flip = True
        elif res <= pertubationProb:
            flip = True
        
        if flip == True:
            if self.status == 1:
                self.status = 0
            else:
                self.status = 1
        
    
    # random bitflips only
    def bitFlipOnlyTimestep(self):
        bitFlipProb = Globals.ranBitFlip

        flip = False
        res = random.random()
        if res <= bitFlipProb:
            flip = True
        
        if flip == True:
            if self.status == 1:
                self.status = 0
            else:
                self.status = 1
    
    # Sisor outage
    def sisorTimestep(self, probability):
        # reset if already experiencing outage
        if self.sisorOutageFlag == True:
            # two comments below changed for sisor outage if statement instead of 0 status if stateement
            #res = random.randint(0, 1)
            #self.status = res
            self.sisorOutageFlag = False
        # new outage chance
        outage = False
        res = random.random()
        if res <= probability:
            #self.status = 0
            self.sisorOutageFlag = True
    
    # clean up after sisor finishes
    def sisorFinish(self):
        # finishes the sisor outage and resets nodes
            if self.sisorOutageFlag == True:
                #res = random.randint(0, 1)
                #self.status = res
                self.sisorOutageFlag = False

    # updates the past status to the current status
    def resetStatus(self):
        if self.status == 0:
            self.pastStatus = 0
        elif self.status ==1:
            self.pastStatus = 1
    
    # update the status of the node
    def updateStatus(self):
        inputNodes = self.inputNodes
        lookupTable = self.lookupDict
        resultArray = []
        
        # looks up the PAST status of the nodes in the input node list (in case they have already updated)
        for node in inputNodes:
            nodeStatus = node.pastStatus
            resultArray.append(nodeStatus)
        # convert array to tuple
        resultTuple = tuple(resultArray)

        if len(lookupTable) > 0 and len(resultTuple) > 0:
            # Lookup new status and update
            lookupStatus = lookupTable[resultTuple]
            node.status = lookupStatus