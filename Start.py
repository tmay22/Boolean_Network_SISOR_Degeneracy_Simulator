# Start script for the simulator

import Setup
import Globals
import hashlib
import datetime


def main():
    print("")
    print("----------------------------------------")
    print("Welcome to the Boolean Network SISOR Degeneracy Simulator!")
    print("----------------------------------------")

    # For now these are hard-coded but these can be queried in future from user
    # numNodes is the number of Nodes in the network. Is only required for base networks
    numNodes = Globals.numNodes
    # Path is the path to the csv input files. Is only required for applied networks
    path = ""
    # 1 = Base | 2 = Applied
    caseType = 1
    Globals.caseType = caseType

    # Make sessionId  
    # Get current datetime as string
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # Convert to bytes
    now_b = now.encode('utf-8')
    # Calculate SHA-256 hash
    hash = hashlib.sha256(now_b)
    # Get hexadecimal digest string (unique hash)
    Globals.sessionId = hash.hexdigest()

    Setup.initiate(path, numNodes, caseType)


if __name__ == "__main__":
     main()