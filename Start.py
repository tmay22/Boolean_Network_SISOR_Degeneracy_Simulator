# Start script for the simulator

import Setup
import Globals


def main():
    print("")
    print("----------------------------------------")
    print("Welcome to the Boolean Network SISOR Degeneracy Simulator!")
    print("----------------------------------------")

    # For now these are hard-coded but these can be queried in future from user
    # numNodes is the number of Nodes in the network. Is only required for base networks
    numNodes = 10
    # Path is the path to the csv input files. Is only required for applied networks
    path = ""
    # 1 = Base | 2 = Applied
    caseType = 1
    Globals.caseType = caseType

    Setup.initiate(path, numNodes, caseType)


if __name__ == "__main__":
     main()