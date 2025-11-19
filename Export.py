import Globals
import csv
import os

# export an individual simulation containing a key, value pair of data in a dictionary into a new file
def expNewDict(fileNamePath, outDict):

    with open(fileNamePath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'Value'])  # header
        for key, value in outDict.items():
            writer.writerow([key, value])

def getMainDictNameDetails():

    details = f'T-All_K{Globals.averageInput}.N{Globals.numNodes}.P{int(Globals.sisorNewNodeProb*100)}'

    id = f'{Globals.sessionId}'

    path = "./Cumulative_Outputs"
    details = str(details)
    file = str(f'{path}/{details}.csv')

    return file, id

def addToDict(fileNamePath, outDict, identifier):

    # check if file exists
    fileExists = os.path.isfile(fileNamePath)

    fieldNames = ["Identifier", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    if not fileExists or os.stat(fileNamePath).st_size==0:
        needsHeader = True
    else:
        needsHeader = False

    with open(fileNamePath, 'a', newline='') as f:
        writer = csv.writer(f)
        if needsHeader:
            writer.writerow(fieldNames)
        # writer.writerow(row)
        # writer = csv.writer(f, field)
        
        rowArray = [identifier]
        lenDict = len(outDict)
        counter = 0
        while counter < lenDict:
            newVal = outDict[counter]
            rowArray.append(newVal)
            counter = counter + 1
        
        writer.writerow(rowArray)
    
    print("Successfully exported")