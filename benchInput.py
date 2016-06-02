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

QUESTION:
    - Where to store Grid size and IOs' location?

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
# initialize the lists
gates = [] 
iosGates = []
ios = []
gatesID = set()
gatesMap = dict()
inCons = {}
outCons = {}
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
    if (len(info) > 0):
        if info[0] == "#":
            #print "comment"
            pass
        elif isNumber(info[0]):
            # NORMAL GATE
            # there will be output in this type of line as well

            # get gate ID
            iden = int(info[0])
            #print iden

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
                #gatesID.add(iden)
                # suppose all gate delay = 1
                newGate = pt.Gate(iden, delay=1, IO=False)
                gatesMap[iden] = newGate 
                inCons[newGate] = set()
                outCons[newGate] = set()
                gates.append(newGate)
            # add the connection
            # now I see the problem, if we want to point to actual gate in the
            # dict, then it's not straightforward
            # Idea: create a map between gateID and actual gate object!
            for fanin in cons:
                gateIn = gatesMap[int(fanin)]
                currGate = gatesMap[iden]
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
            # build the io gate
            newGate = pt.Gate(iden, delay=0, IO=True)
            gates.append(newGate)
            #gatesID.add(iden)
            gatesMap[iden] = newGate
            #ios.append(newGate)
            #iosGates.add(newGate)
            inCons[newGate] = set()
            outCons[newGate] = set()
            
#print gatesMap
#print inCons

# done reading file
f.close()

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


