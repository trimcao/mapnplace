"""
Reading user data from text file for Mapping and Placement algorithm.

Name: Tri Minh Cao
email: tricao@utdallas.edu
Date: May 2016
"""

import placeTree as pt

# create gate list and ios list
# NOTE: later, input test file name by user
filename = raw_input('Enter the input file name: ')
print
# initialize the lists
gates = []
ios = []
f = open(filename, "r")
# read the number of gates
numGates = int(f.readline().split()[0])
for i in range(numGates):
    info = f.readline()
    # remove spaces and newline
    info = info.split()
    gateName = info[0]
    gateDelay = int(info[1])
    isIO = False
    if (info[2] == 'True'):
        isIO = True
        IOLoc = (int(info[3]), int(info[4]))
    # initialize the gate
    newGate = pt.Gate(gateName, gateDelay, isIO)
    gates.append(newGate)
    if (isIO):
        ios.append((newGate, IOLoc))

# make inCons and outCons dictionaries and create a Grid object
inCons = {}
outCons = {}
for gate in gates:
    inCons[gate] = set()
    outCons[gate] = set()

for line in f:
    info = line.split()
    originID = int(info[0])
    if (len(info) > 1):
        for i in range(1, len(info)):
            destID = int(info[i])
            outCons[gates[originID]].add(gates[destID])
            inCons[gates[destID]].add(gates[originID])
# done reading file
f.close()

# Try test1.txt data
gridTest1 = pt.Grid(4, 5, ios, gates, inCons, outCons)

# test Placement
testPlace1 = pt.Placement(gridTest1, pt.manhattanDelay)
testPlace1.buildTables()
for each in testPlace1._gates:
    print testPlace1.delayTableToStr(each)
# placement from delay tables
testPlace1.place()
print testPlace1._grid
