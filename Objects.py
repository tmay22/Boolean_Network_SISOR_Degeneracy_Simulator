# Contains the object classes
import uuid
import random
import Globals

# Represents a Node in the network
class Node:

    def __init__(self):
        self.id = uuid.uuid4()
        # inputNodes is expected to be a list of Nodes
        self.inputNodes = []
        # lookup output table
        self.lookupDict = {}
        self.domain = None
        if Globals.caseType == 1:
            self.randDomain()
        # Set status to 1 by default
        self.status = 1
    
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