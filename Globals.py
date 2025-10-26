# Globals variables for the simulator

# The type of case for the simulator
# 1 = "Base" case where nodes do not have names
# 2 = "Applied" case where nodes do have names
global caseType
caseType = 0

# Dictionary of all nodes at setup state
global nodeDict
nodeDict = {}

# Dictionary of nodes after the sisor application
global sisorDict
sisorDict = {}

# avaerage number of inputs per node (mean K value)
global averageInput
averageInput = 1


# random chance of a bit flip occuring per timestep
global ranBitFlip
ranBitFlip = 0.05

# pertubation chance via injection of bit flip
global pertubation
pertubation = 0.25

# counter of indexes
global indexCounter
indexCounter = 0


# SISOR conflict decision point
global sisorConflictDp
sisorConflictDp = 0.93

# SISOR maximum level of acceptable degradation
global sisorMaxDegradation
sisorMaxDegradation = 0.3

# SISOR sensitivity to conflict
global sisorSensConflict
sisorSensConflict = 10

# SISOR conflict likelihood
global sisorConflictProb
sisorConflictProb = 0.9

# SISOR new node likelihood (alt to new connection)global sisorNewNodeProb
global sisorNewNodeProb
sisorNewNodeProb = 1

# change log to record changes to the network
global changeLog
changeLog = []