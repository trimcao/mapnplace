"""
Input for Mapping and Placement algorithm
using ISCAS85 format

Name: Tri Minh Cao
email: tricao@utdallas.edu
Date: May 2016
"""
import math
import random
import placeTree as pt
import delayLookup as dl

"""
QUESTION:
    - Where to store Grid size and IOs' location?
        - Answer: randomize first
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
filename = "test1.bench"
#filename = "c17.bench"
#filename = "c432.bench"
#filename = "c880.bench"
# initialize the lists
# assume gates is a list of gatesID, not actual gates
# it seems we don't need gates list because we can get a list gates from
# gatesMap.keys()
gates = []
ios = []
inputs = []
outputs = []
#gatesID = set()
gatesMap = dict()
inCons = {}
outCons = {}
f = open(filename, "r")
# read all lines in one loop
# two types of line: input/output and normal gate.
for line in f:
    info = line
    # remove spaces and newline
    info = info.split()
    if (len(info) > 0):
        if info[0] == "#":
            # NOTE: maybe users will not have a space between '#' and comment
            #print "comment"
            pass
        elif isNumber(info[0]):
            # NORMAL GATE
            # get gate ID
            iden = int(info[0])
            # get gate type
            name = ''
            typeNCons = info[2]
            for i in range(len(typeNCons)):
                if (typeNCons[i] != '('):
                    name += typeNCons[i]
                else:
                    signIdx = i
                    break
            # combine all connections info
            consInfo = ''
            for i in range(2, len(info)):
                consInfo += info[i]
            # get connections
            cons = ''
            for i in range(signIdx + 1, len(consInfo)):
                if (consInfo[i] != ')'):
                    cons += consInfo[i]
                else:
                    break
            # split again using ','
            cons = cons.split(',')
            # now each fan-in is an element of the cons array
            # create the gate
            if (not iden in gatesMap):
                # get the delay of the cell from lookup table
                gateDelay = dl.table[name]
                newGate = pt.Gate(iden, delay=gateDelay, IO=False)
                gatesMap[iden] = newGate
                inCons[newGate.getID()] = set()
                outCons[newGate.getID()] = set()
                #gates.append(newGate)
            # add the connection
            for fanin in cons:
                gateIn = int(fanin)
                currGate = iden
                inCons[currGate].add(gateIn)
                outCons[gateIn].add(currGate)

        else:
            # IO case:
            # get io gate name
            # get input and output
            txtOrg = info[0]
            name = ''
            for i in range(len(txtOrg)):
                if (txtOrg[i] != '('):
                    name += txtOrg[i]
                else:
                    signIdx = i
                    break
            # get ID
            iden = ''
            for i in range(signIdx + 1, len(txtOrg)):
                if (txtOrg[i] != ')'):
                    iden += txtOrg[i]
                else:
                    break
            iden = int(iden)
            if (name=='INPUT'):
                inputs.append(iden)
            else:
                outputs.append(iden)
            # build the io gate
            newGate = pt.Gate(iden, delay=0, IO=True)
            #gates.append(newGate)
            gatesMap[iden] = newGate
            #ios.append(newGate)
            inCons[newGate.getID()] = set()
            outCons[newGate.getID()] = set()

# done reading file
f.close()

print inCons
print outCons

"""
#The following code only works for the "test1.bench" test

# create ios list
# input 1: (0, 0)
# input 2: (0, 3)
# output: (4, 1)
ios.append((gatesMap[1], (0,0)))
ios.append((gatesMap[2], (0, 3)))
#ios.append((gatesMap[22], (4, 1)))
ios.append((gatesMap[22], (1, 3)))

# Try test1.bench data
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

# need to do the following things:
# randomize the dimensions
# choose locations for ios
# test with other test benches
# NOTE: these test benches might not be trees
# Shit: the algorithm really only works with trees
# - Need to be able to check if the circuit is a tree, amd a DAG.


# dimensions: possibly square for easy test, sqrt(#gates*6)
numGates = len(gatesMap)
#print numGates
dim = int(math.sqrt(numGates * 2))
#print dim

# choose locations for ios
# input will be at some location in the first column
# output will be at some location in the last column

#print type(gates[0].getID())


for each in inputs:
    row = random.randrange(0, dim)
    #ios.append((gatesMap[each], (0, row)))
    ios.append((each, (0, row)))
for each in outputs:
    row = random.randrange(0, dim)
    #ios.append((gatesMap[each], (dim - 1, row)))
    ios.append((each, (dim - 1, row)))


# Try test1.bench data
gridTest = pt.Grid(dim, dim, ios, gatesMap, inCons, outCons)
gridTest.topoSort()
print gridTest._gates

# test Placement
testPlace = pt.Placement(gridTest, pt.manhattanDelay)
testPlace.buildTables()
for each in testPlace._gates:
    print testPlace.delayTableToStr(each)
# placement from delay tables
testPlace.place()
print testPlace._grid


# Possible solutions:
# - do not use complex object as dictionary: gate object, tuple, etc.
# The best key type is integer.
# - avoid using dict altogether, because all gates are integer


# OUTPUT TO FILES
# What should we output:
# All delay tables: Gate name, then delay table. Might align later. 
# Gate placement: just simple - gate [space] location (col, row)
for each in testPlace._gatesPlace:
    print str(each) + ' ' + str(testPlace._gatesPlace[each])

fileOut = open('test1.out', 'w')

for each in testPlace._gates:
    fileOut.write('Gate ' + str(each) + ' delay table: \n')
    fileOut.write(testPlace.delayTableToStr(each))
    fileOut.write('\n')
fileOut.write('Final placement: \n')
for each in testPlace._gatesPlace:
    fileOut.write(str(each) + ' ' + str(testPlace._gatesPlace[each]))
    fileOut.write('\n')

