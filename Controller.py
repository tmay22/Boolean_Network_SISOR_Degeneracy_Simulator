# Controller script for the simulator
import DegeneracySim
import Globals
import Sisor
import Graph

def mainMenu():
    run = True
    while run:
        # Preamble and initial option selection
        print("----------------------------------------")        
        print("What would you like to do?")
        print("----------------------------------------")
        print("(1) Original System Degeneracy")
        print("(2) SISOR then Degeneracy")
        print("(3) Graph Original Network")
        print("(4) Graph SISOR Network")
        mainMenuOp= input("Choose Option: ")
        print("You Selected " + mainMenuOp)

        # Setup Option division
        if mainMenuOp == "1":
            # Calculate degeneracy of default system  AND REDUNDANCY
            DegeneracySim.getDegeneracy(Globals.nodeDict)
            DegeneracySim.getRedundancy(Globals.nodeDict)
            
        if mainMenuOp == "2":
            # Apply SISOR and then calculate degeneracy AND REDUNDANCY
            if len(Globals.sisorDict)>0:
                Sisor.sisorIntro(Globals.sisorDict)
            else:
                Sisor.sisorIntro(Globals.nodeDict)
        if mainMenuOp == "3":
            # graph the original network
            Graph.graphNetwork(Globals.nodeDict)
        if mainMenuOp == "4":
            # graph the sisor network
            Graph.graphNetwork(Globals.sisorDict)


