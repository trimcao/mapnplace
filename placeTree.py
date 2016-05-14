"""
PlaceTree algorithm in the paper by Yifang Liu et. al.

Name: Tri Minh Cao
Email: tricao@utdallas.edu
Date: April 2016
"""

# NOTE: what I need to do: optimize the code, add user input feature (user can
# add a grid and add input and output

class Gate:
    """
    this class represents a gate in the circuits
    parameters include: delay, arrival time, etc.
    """
    def __init__(self, name, delay = 0, IO = False):
        self._name = name
        # in the program, we will initialize all gates first, then we add
        # information about connections

        # initialize inputs and outputs
        self._inputs = set() # use set to prevent duplication
        self._outputs = set()
        self._delay = delay
        self._isIO = IO

    def __str__(self):
        return self._name

    def isIO(self):
        return self._isIO

    def getDelay(self):
        return self._delay

class TopoSort:
    """
    TopoSort class to sort the gates topologically
    """
    def __init__(self):
        self.unvisited = set()
        self.visited = set()
        self.tempVisited = set() # later
        self.result = []

    def sort(self, gates, outputs):
        """
        Sort the gates topologically based on outputs
        Input: gates is the list of gates; outputs is a dict containing inter-
        connections data of these gates
        Note: probably we need a class to do topoSort properly
        Need to add temporary marked
        """
        self.unvisited = set(gates)
        self.visited = set()
        self.tempVisited = set() # later
        self.result = []
        while (len(self.unvisited) > 0):
            currentGate = self.unvisited.pop()
            #print outputs
            self.visit(currentGate, outputs)
        return self.result

    def visit(self, gate, outputs):
        if not (gate in self.visited):
            # check if key 'gate' existed in the outputs dict
            if (gate in outputs):
                for each in outputs[gate]:
                    self.visit(each, outputs)
            self.visited.add(gate)
            self.result.insert(0, gate)

"""
# examples of gates
g1 = Gate('g1')
g2 = Gate('g2')
g3 = Gate('g3')
g4 = Gate('g4')
g5 = Gate('g5')

#print g1
#print g2

# add inputs and outputs
g1.addOut(g3)
g3.addOut(g5)
g2.addOut(g4)
g4.addOut(g5)
outputs = {}
outputs[g1] = set([g3])
outputs[g3] = set([g5])
outputs[g2] = set([g4])
outputs[g4] = set([g5])

#print g3._outputs

gates = [g5, g3, g2, g4, g1]
#topoSort(gates)
topoSorter = TopoSort()
result = topoSorter.sort(gates, outputs)
for each in result:
    print each
"""

class Grid:
    """
    class Grid consists of a 2d array to represent the Grid
    the class also takes care of positioning of gates, and position of IO nodes
    Grid will contain the interconnection data between gates
    """
    def __init__(self, height, width, ios, gates, inCons = {}, outCons = {}):
        """
        IOs are represented as gates with fixed positions
        inputs and outputs are list of IOs and their positions (as tuple)
        gates is a list of gates, excluding the IOs
        We represent the grid by a 2d list, each position in the grid, in turn,
        is a list of gates (one position may have multiple gates).

        ios: list of IOs gates and locations
        inCons and outCons: dicts of interconnections of the gates, these dicts
            can be provided during initialization.
        """
        self._height = height
        self._width = width
        self._grid = [[set() for i in range(height)] for j in range(width)]
        #self._inputs = inputs
        #self._outputs = outputs
        self._IOLocs = dict()
        # NOTE: probably don't need to differentiate inputs from outputs, they
        # work the same
        # process inputs and outputs
        for each in ios:
            self._IOLocs[each[0]] = each[1]
        # NOTE: also need to store the locations of all gates
        self._locs = dict()
        self._gates = gates
        self._gates.extend(self._IOLocs.keys())
        # Note: current idea is to build delay tables for all gates, including
        # IOs

        self._inCons = inCons
        self._outCons = outCons

        # we need to sort each time we do a new placement
        self._topoSorter = TopoSort()
        # NOTE: must re-write the following line. Must initialize the interconnections
        # within Grid class.
        #self._gates = topoSorter.sort(self._gates, outputs)

    def __str__(self):
        s = ''
        height = self.getHeight()
        width = self.getWidth()
        for i in range(height):
            for j in range(width):
                if len(self._grid[j][i]) > 0:
                    for gate in self._grid[j][i]:
                        s = s + str(gate) + ','
                else:
                    s += 'x'
                s += '    '
            s += '\n'
        return s

    def fill(self, gate, col, row):
        # only use this method at the end of placement process
        self._grid[col][row].add(gate)
        self._locs[gate] = (col, row)

    def getHeight(self):
        return self._height

    def getWidth(self):
        return self._width

    def getGates(self):
        return self._gates

    def getIOLoc(self, IO):
        return self._IOLocs[IO]

    def getLoc(self, gate):
        return self._locs[gate]

    def addIn(self, gate, inp):
        if gate in self._inCons:
            self._inCons[gate].add(inp)
        else:
            self._inCons[gate] = set([inp])

    def addOut(self, gate, out):
        if gate in self._outCons:
            self._outCons[gate].add(out)
        else:
            self._outCons[gate] = set([out])

    def numIn(self, gate):
        if gate in self._inCons:
            return len(self._inCons[gate])
        else:
            return 0

    def numOut(self, gate):
        if gate in self._outCons:
            return len(self._outCons[gate])
        else:
            return 0

    def getOutputs(self, gate):
        if gate in self._outCons:
            return self._outCons[gate]
        else:
            return set()

    def getInputs(self, gate):
        if gate in self._inCons:
            return self._inCons[gate]
        else:
            return set()

    def topoSort(self):
        self._gates = self._topoSorter.sort(self._gates, self._outCons)


# Examples of IOs
# Note: the position rule in the paper is based on x-y cartesian axis (weird)
# however, I think it will be fine
# Also, the first row is 1, not 0. It should be ok I believe
in1 = Gate("I1", IO = True)
in2 = Gate("I2", IO = True)
v1 = Gate("v1", delay = 1)
v2 = Gate("v2", delay = 1)
v3 = Gate("v3", delay = 1)
out = Gate("O", IO = True)

gatesExam = [v1, v2, v3]
#inputs = [(in1, (0, 0)), (in2, (0, 3))]
#outputs = [(out, (4, 1))]
ios = [(in1, (0, 0)), (in2, (0, 3)), (out, (4, 1))]


# test Grid class
gridTest = Grid(4, 5, ios, gatesExam)
#for each in gridTest._IOLocs.keys():
#    print each
#print gridTest._IOLocs
#for each in gridTest._gates:
#    print each

# interconnections
gridTest.addOut(v1, v3)
gridTest.addOut(v2, v3)
gridTest.addIn(v3, v1)
gridTest.addIn(v3, v2)

gridTest.addOut(v3, out)
gridTest.addIn(out, v3)
gridTest.addOut(in1, v1)
gridTest.addOut(in2, v2)
gridTest.addIn(v1, in1)
gridTest.addIn(v2, in2)

#gridTest.topoSort()
#for each in gridTest.getGates():
#    print each

#print gridTest._outCons

class Placement:
    """
    class Placement takes a grid object as an input, then a build delay table for
    each gate existed in the grid.
    It will return an grid with gates in optimal locations.
    """
    def __init__(self, grid, delayModel):
        self._grid = grid
        self._delayModel = delayModel
        self._delayTables = dict()
        # probably delay table should be a dict, not a 2d array
        self._locations = []
        for i in range(grid.getWidth()):
            for j in range(grid.getHeight()):
                self._locations.append((i, j))
        #table = [[float('inf') for i in range(grid.getHeight())] for j in range(grid.getWidth())]
        # call topoSort
        self._grid.topoSort()
        self._gates = grid.getGates()
        self._locOpt = dict()
        #self._possibleLocs = dict()
        for each in self._gates:
            self._delayTables[each] = dict()
            # initialize the locOpt
            self._locOpt[each] = dict()
            for loc in self._locations:
                self._locOpt[each][loc] = dict()

    def getLocations(self):
        return self._locations

    def setLocOpt(self, outGate, locOut, inGate, locIn):
        self._locOpt[outGate][locOut][inGate] = locIn

    def setDelay(self, gate, loc, delay):
        self._delayTables[gate][loc] = delay

    def buildTables(self):
        """
        Method to build delay tables for each gate
        """
        # call topoSort
        self._grid.topoSort()
        self._gates = self._grid.getGates()
        height = self._grid.getHeight()
        width = self._grid.getWidth()
        locations = self.getLocations()
        possibleLocs = []
        for each in self._gates:
            # Need to find a way to store locations of fanins
            # idea: each gate will have another dict. Format of information:
            # locOpt[currentGate][loc][fanin] = optimal loc for that fanin
            # inside locOpt[currentGate] is another dict
            if each.isIO():
                possibleLocs = [self._grid.getIOLoc(each)]
            else:
                possibleLocs = locations
            # process each possible location
            for loc in possibleLocs:
                # initialize to find the maxDelay
                maxDelay = each.getDelay()
                for fanin in self._grid.getInputs(each):
                #for fanin in each.getInputs():
                    minDelay = float('inf')
                    minInLoc = (-1, -1)
                    # probably we only need to consider the locations present
                    # in the delay table
                    for inLoc in self._delayTables[fanin].keys():
                        inDelay = self._delayTables[fanin][inLoc]
                        delay = inDelay + self._delayModel(loc, inLoc) + each.getDelay()
                        # find the min delay
                        # NOTE: we might have multiple minDelay, that leads to
                        # multiple solutions
                        if (delay <= minDelay):
                            minDelay = delay
                            minInLoc = inLoc
                    # remember the optimal location for the fanin
                    self.setLocOpt(each, loc, fanin, minInLoc)
                    # update the maxDelay
                    if (minDelay > maxDelay):
                        maxDelay = minDelay
                # update delay for current loc in delay table
                self.setDelay(each, loc, maxDelay)

    def getDelayTable(self, gate):
        table = [[float('inf') for i in range(self._grid.getHeight())] for j in range(self._grid.getWidth())]
        for loc in self._delayTables[gate].keys():
            table[loc[0]][loc[1]] = self._delayTables[gate][loc]
        return table

    def getOptLoc(self, outGate, locOut, inGate):
        return self._locOpt[outGate][locOut][inGate]

    def place(self):
        # idea: for IOs, just put them to their fixed positions
        for i in range(len(self._gates) - 1, -1, -1):
            currentGate = self._gates[i]
            if (currentGate.isIO()):
                loc = self._grid.getIOLoc(currentGate)
                self._grid.fill(currentGate, loc[0], loc[1])
            else:
                fanout = list(self._grid.getOutputs(currentGate))[0] # we are only dealing with trees
                if (fanout.isIO()):
                    fanoutLoc = self._grid.getIOLoc(fanout)
                else:
                    fanoutLoc = self._grid.getLoc(fanout)
                loc = self.getOptLoc(fanout, fanoutLoc, currentGate)
                self._grid.fill(currentGate, loc[0], loc[1])


def manhattanDelay(loc1, loc2):
    """
    Manhattan Delay model
    Delay between two nodes = square of manhattan distance between the nodes
    """
    x1 = loc1[0]
    y1 = loc1[1]
    x2 = loc2[0]
    y2 = loc2[1]
    return (abs(x2 - x1) + abs(y2 - y1))**2

#placeTest = Placement(gridTest, manhattanDelay)
#for each in placeTest._delayTables.keys():
#    print each

# test Placement

testPlace = Placement(gridTest, manhattanDelay)
testPlace.buildTables()
for each in testPlace._gates:
    table = testPlace.getDelayTable(each)
    #for i in range(len(table)):
    #    print table[i]
    #print
    # print
    s = ''
    for row in range(len(table[0])):
        for col in range(len(table)):
          s = s + str(table[col][row]) + '  '
        s += '\n'
    print s
    print

# try to compute by hand
#print testPlace._delayTables[v1][(0, 0)]
testPlace.place()
print testPlace._grid

# NOTE: I probably have to correct result now, it is different from the example
# in the paper but the two solutions are both correct
