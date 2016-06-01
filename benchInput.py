"""
Input for Mapping and Placement algorithm
using ISCAS85 format

Name: Tri Minh Cao
email: tricao@utdallas.edu
Date: May 2016
"""

import placeTree as pt

"""
IDEA:
    - Don't read line with comment #
    - Read Input and Outputs without locations
    - Assume 'NAND' is just a gate with constant delay. We will do something
    with different gates later.
    - We will build inCons list on-the-fly
"""

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# create gate list and ios list
#filename = raw_input('Enter the input file name: ')
#print
filename = "c17.bench"
# initialize the lists
gates = []
ios = []
f = open(filename, "r")
# read all lines in one loop
# two types of line: input/output and normal gate. 
# probably use two separate methods to deal with these two types above is a
# good move

# important line: 
# newGate = pt.Gate(gateName, gateDelay, isIO)
# ios.append((newGate, IOLoc))
for line in f:
    info = line
    # remove spaces and newline
    info = info.split()
    print info
    if (len(info) > 0):
        if info[0] == "#":
            print "comment"
        elif isNumber(info[0]):
            print "normal gate"
        else:
            print "io"

"""
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
"""

