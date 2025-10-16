# Contains the object classes
import uuid
import random
import Globals

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
            self.status = 1
            self.sisorOutageFlag = False
        # new outage chance
        outage = False
        res = random.random()
        if res <= probability:
            self.status = 0
            self.sisorOutageFlag = True
    
    # updates the past status to the current status
    def resetStatus(self):
        if self.status == 0:
            self.pastStatus = 0
        elif self.status ==1:
            self.pastStatus = 1