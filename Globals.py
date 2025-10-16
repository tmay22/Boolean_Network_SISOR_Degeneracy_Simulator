# Globals variables for the simulator

# The type of case for the simulator
# 1 = "Base" case where nodes do not have names
# 2 = "Applied" case where nodes do have names
global caseType
caseType = 0

# Dictionary of all nodes at setup state
global nodeDict
nodeDict = {}

# avaerage number of inputs per node (mean K value)
global averageInput
averageInput = 2


# random chance of a bit flip occuring per timestep
global ranBitFlip
ranBitFlip = 0.05

# pertubation chance via injection of bit flip
global pertubation
pertubation = 0.25

# counter of indexes
global indexCounter
indexCounter = 0


