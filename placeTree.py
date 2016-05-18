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
    Interconnections between gates will be handled by Grid class.
    """
    def __init__(self, name, delay = 0, IO = False):
        self._name = name
        # initialize inputs and outputs
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
        input: gates is the list of gates; outputs is a dict containing inter-
        connections data of these gates
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

        height and width: dimensions of the grid
        gates: a list of gates in the grid
        ios: list of IOs gates and locations
            format: a tuple (IOgate, location tuple)
        inCons and outCons: dicts of interconnections of the gates, these dicts
            can be provided during initialization.
        """
        self._height = height
        self._width = width
        self._grid = [[set() for i in range(height)] for j in range(width)]
        self._IOLocs = dict()
        # process inputs and outputs
        for each in ios:
            self._IOLocs[each[0]] = each[1]
        # store the locations of all gates in the locs dict
        self._locs = dict()
        self._gates = gates
        # add IOs to the self._gates list
        #self._gates.extend(self._IOLocs.keys())
        # NOTE: may be a better idea to initialize the inCons and outCons with
        # all gates in the grid.
        self._inCons = inCons
        self._outCons = outCons
        # we need to sort each time we do a new placement
        self._topoSorter = TopoSort()

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
        """
        This method is used to add a gate to a location in the resulting grid.
        """
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
        """
        Return the location of a gate
        """
        return self._locs[gate]

    def addIn(self, gate, inp):
        """
        Add a fanin of a gate
        """
        if gate in self._inCons:
            self._inCons[gate].add(inp)
        else:
            self._inCons[gate] = set([inp])

    def addOut(self, gate, out):
        """
        Add a fanout of a gate
        """
        if gate in self._outCons:
            self._outCons[gate].add(out)
        else:
            self._outCons[gate] = set([out])

    def numIn(self, gate):
        """
        Return number of fanins of a gate
        """
        if gate in self._inCons:
            return len(self._inCons[gate])
        else:
            return 0

    def numOut(self, gate):
        """
        Return number of fanouts of a gate
        """
        if gate in self._outCons:
            return len(self._outCons[gate])
        else:
            return 0

    def getOutputs(self, gate):
        """
        Return the fanouts of a gate as a list.
        """
        if gate in self._outCons:
            return self._outCons[gate]
        else:
            return set()

    def getInputs(self, gate):
        """
        Return the fanins of a gate as a list.
        """
        if gate in self._inCons:
            return self._inCons[gate]
        else:
            return set()

    def topoSort(self):
        """
        Call the topological sort method.
        """
        self._gates = self._topoSorter.sort(self._gates, self._outCons)


class Placement:
    """
    class Placement takes a grid object as an input, then build a  delay table for
    each gate existed in the grid.
    It will return an grid with gates in optimal locations.
    """
    def __init__(self, grid, delayModel):
        """
        grid: the grid needed to do placement
        delayModel: the function used to compute the delay between two gates
        """
        self._grid = grid
        self._delayModel = delayModel
        # represent the delay tables by dictionaries
        self._delayTables = dict()
        self._locations = []
        for i in range(grid.getWidth()):
            for j in range(grid.getHeight()):
                self._locations.append((i, j))
        # call topoSort to sort the gates topologically
        self._grid.topoSort()
        self._gates = grid.getGates()
        # initialize the locOpt, a dict to store the optimal location for each gate
        self._locOpt = dict()
        for each in self._gates:
            self._delayTables[each] = dict()
            self._locOpt[each] = dict()
            for loc in self._locations:
                self._locOpt[each][loc] = dict()

    def getLocations(self):
        """
        Return all possible locations from the grid as a list
        """
        return self._locations

    def setLocOpt(self, outGate, locOut, inGate, locIn):
        """
        Set the optimal location for the fanin while doing placement
        """
        self._locOpt[outGate][locOut][inGate] = locIn

    def setDelay(self, gate, loc, delay):
        """
        Set the optimal delay for a location in the delay table
        """
        self._delayTables[gate][loc] = delay

    def buildTables(self):
        """
        Method to build delay tables for each gate
        """
        # call topoSort
        self._grid.topoSort()
        # need to update the self._gates because the sorting method only sort
        # the gate list in the Grid object.
        self._gates = self._grid.getGates()
        height = self._grid.getHeight()
        width = self._grid.getWidth()
        locations = self.getLocations()
        possibleLocs = []
        for each in self._gates:
            # each gate will have another dict. Format of information:
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
                    minDelay = float('inf')
                    minInLoc = (-1, -1)
                    # we only need to consider the locations present in the delay table
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
        """
        Get the delay table in list format
        """
        table = [[float('inf') for i in range(self._grid.getHeight())] for j in range(self._grid.getWidth())]
        for loc in self._delayTables[gate].keys():
            table[loc[0]][loc[1]] = self._delayTables[gate][loc]
        return table

    def getOptLoc(self, outGate, locOut, inGate):
        return self._locOpt[outGate][locOut][inGate]

    def place(self):
        """
        This method will do the actual placement using the delay tables.
        """
        for i in range(len(self._gates) - 1, -1, -1):
            currentGate = self._gates[i]
            # put the IOs to their fixed location
            if (currentGate.isIO()):
                loc = self._grid.getIOLoc(currentGate)
                self._grid.fill(currentGate, loc[0], loc[1])
            else:
                #print currentGate
                #print self._grid.getOutputs(currentGate)
                fanout = list(self._grid.getOutputs(currentGate))[0] # we are only dealing with trees
                if (fanout.isIO()):
                    fanoutLoc = self._grid.getIOLoc(fanout)
                else:
                    fanoutLoc = self._grid.getLoc(fanout)
                loc = self.getOptLoc(fanout, fanoutLoc, currentGate)
                self._grid.fill(currentGate, loc[0], loc[1])

    def delayTableToStr(self, gate):
        table = self.getDelayTable(gate)
        s = ''
        for row in range(len(table[0])):
            for col in range(len(table)):
                s = s + str(table[col][row]) + '  '
            s += '\n'
        return s

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

# NOTE: I probably have to correct result now, it is different from the example
# in the paper but the two solutions are both correct
