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
gatesID = set()
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
            #print "normal gate"
            # there will be output in this type of line as well

            # get gate ID
            iden = int(info[0])
            #print iden
            #if (not iden in gatesID):
            #    gatesID.add(iden)

            # get gate type
            name = ''
            typeNCons = info[2]
            for i in range(len(typeNCons)):
                if (typeNCons[i] != '('):
                    name += typeNCons[i]
                else:
                    signIdx = i
                    break
            print name

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
            print cons
            # now each fan-in  is an element of the cons array 

        else:
            #print "io"
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
            #print iden

            # build the io gate
            newGate = pt.Gate(iden, delay=0, IO=True)
            gates.append(newGate)
            gatesID.add(iden)
            #IOLoc?
            #ios.append(newGate)

            


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

