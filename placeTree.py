"""
PlaceTree algorithm in the paper by Yifang Liu et. al.

Name: Tri Minh Cao
Email: tricao@utdallas.edu
Date: April 2016
"""

# first, implement a draft class Gate and write a topological sort method

class Gate:
    """
    this class represents a gate in the circuits
    parameters include: inputs, outputs, delay, ...
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

    def addIn(self, inp):
        self._inputs.add(inp)

    def addOut(self, out):
        self._outputs.add(out)

    def numIn(self):
        return len(self._inputs)

    def numOut(self):
        return len(self._outputs)

    def getOutputs(self):
        return self._outputs


class TopoSort:
    """
    TopoSort class to sort the gates topologically
    """

    def __init__(self):
        self.unvisited = set()
        self.visited = set()
        self.tempVisited = set() # later
        self.result = []

    def sort(self, gates):
        """
        Sort the gates topologically based on outputs

        Note: probably we need a class to do topoSort properly
        Need to add temporary marked
        """
        self.unvisited = set(gates)
        self.visited = set()
        self.tempVisited = set() # later
        while (len(self.unvisited) > 0):
            currentGate = self.unvisited.pop()
            self.visit(currentGate)
        return self.result

    def visit(self, gate):
        if not (gate in self.visited):
            for each in gate.getOutputs():
                self.visit(each)
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

#print g3._outputs

gates = [g5, g3, g2, g4, g1]
#topoSort(gates)
topoSorter = TopoSort()
result = topoSorter.sort(gates)
for each in result:
    print each
"""
# May 04, 2016: implement delay table for each of the gates
# how do we do the placement? we will build a delay table for each gate
# where do we store the delay table? Probably we will use another class called
# Placement class. How about Mapping?

# Mapping and Placement algo is a modified version of Placement algo, so
# it will live separately.
# Mapping and Placement has two phases: Matching and Covering. Covering is
# very simple. I think I got the main idea behind it.

# We need classes like Grid and Gate to work with different placement algorithms.
# So we cannot keep the delay table inside Grid.
# Since IOs and their positions are specific to one grid, we keep them in
# Grid class

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

# interconnections
v1.addOut(v3)
v2.addOut(v3)
v3.addIn(v1)
v3.addIn(v2)
v3.addOut(out)
out.addIn(v3)
in1.addOut(v1)
in2.addOut(v2)
v1.addIn(in1)
v2.addIn(in2)
gatesExam = [v1, v2, v3]
inputs = [(in1, (0, 0)), (in2, (0, 3))]
outputs = [(out, (4, 1))]


class Grid:
    """
    class Grid consists of a 2d array to represent the Grid
    the class also takes care of positioning of gates, and position of IO nodes
    """
    def __init__(self, height, width, inputs, outputs, gates):
        """
        IOs are represented as gates with fixed positions
        inputs and outputs are list of IOs and their positions (as tuple)
        gates is a list of gates, excluding the IOs
        We represent the grid by a 2d list, each position in the grid, in turn,
        is a list of gates (one position may have multiple gates).
        """
        self._height = height
        self._width = width
        self._grid = [[set() for i in range(height)] for j in range(width)]
        #self._inputs = inputs
        #self._outputs = outputs
        self._IOLocs = dict()
        # process inputs
        for each in inputs:
            self._IOLocs[each[0]] = each[1]
        # process outputs
        for each in outputs:
            self._IOLocs[each[0]] = each[1]
        self._gates = gates
        self._gates.extend(self._IOLocs.keys())
        # Note: current idea is to build delay tables for all gates, including
        # IOs
        topoSorter = TopoSort()
        self._gates = topoSorter.sort(self._gates)

    def __str__(self):
        return str(self._grid)

    def fill(self, gate, col, row):
        # only use this method at the end of placement process
        self._grid[col][row].add(gate)

    def getHeight(self):
        return self._height

    def getWidth(self):
        return self._width

    def getGates(self):
        return self._gates

# test Grid class
gridTest = Grid(4, 5, inputs, outputs, gatesExam)
#for each in gridTest._IOLocs.keys():
#    print each
#print gridTest._IOLocs
#for each in gridTest._gates:
#    print each

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
        table = [[float('inf') for i in range(grid.getHeight())] for j in range(grid.getWidth())]
        self._gates = grid.getGates()
        for each in self._gates:
            self._delayTables[each] = table


def manhattanDelay(x1, y1, x2, y2):
    """
    Manhattan Delay model
    Delay between two nodes = square of manhattan distance between the nodes
    """
    return (x2 - x1)**2 + (y2 - y1)**2

placeTest = Placement(gridTest, manhattanDelay)
for each in placeTest._delayTables.keys():
    print each

# Next: delay table building algo
