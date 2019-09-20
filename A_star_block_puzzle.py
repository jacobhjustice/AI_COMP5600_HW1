from enum import Enum
from queue import PriorityQueue

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Enqueued(Enum):
    NOT_QUEUED = 1
    OPEN = 2
    CLOSED = 3

WHITE_SPACE = -666
BLACK_SPACE = -5

def findWhitespaceNode(nodes):
    nodes.sort(key = lambda x: x.value)
    return nodes[0]


def findNodeByValue(nodes, value):
    nodes.sort(key = lambda x: x.value)
    # Add 5 to value for 1 white space and 4 black spaces
    # subtract 1 from value for index offset
    index = value + 5 - 1
    if value == BLACK_SPACE:
        return None
    if value == WHITE_SPACE:
        return nodes[0]
    return nodes[index]

def findNodeByCoordinates(nodes, x, y):
    if x < 0 or y < 0 or x > 4 or y > 4:
        return None
    nodes.sort(key = lambda x: (x.posX, x.posY))
    index = x * 5 + y
    node = nodes[index]
    return node

class Node:
    def __init__(self, value, posX, posY):
        self.value = value
        self.posX = posX
        self.posY = posY

    def __str__(self):
        return str(self.value) + " ----- " + str(self.posX) + "," + str(self.posY)

    def distanceTo(self, node):
        return abs(self.posX - node.posX) + abs(self.posY - node.posY)

    def swapNodes(self, node):
        if node.value == BLACK_SPACE or self.value == BLACK_SPACE:
            return
        tempX = node.posX
        tempY = node.posY

        node.posX = self.posX
        node.posY = self.posY

        self.posX = tempX
        self.posY = tempY

    def copy(self):
        return Node(self.value, self.posX, self.posY)

class State:
    def __init__(self, g, predecessor, nodes):
        self.g = g
        self.predecessor = predecessor
        self.enqueued = Enqueued.NOT_QUEUED
        self.nodes = nodes
    
    def f(self):
        return self.g + self.h()

    def h(self):
        d = 0
        for n in self.nodes:
            d += self.evaluateDistanceToGoal(n)
        return d

    def copyNodes(self):
        nodes = []
        for n in self.nodes:
            nodes.append(n.copy())
        return nodes

    def nextState(self, nodeToSwap):
        nodes = self.copyNodes()
        w = findWhitespaceNode(nodes)
        n = findNodeByCoordinates(nodes, nodeToSwap.posX, nodeToSwap.posY)

        n.swapNodes(w)
        state = State(self.g + 1, self, nodes)

        return state
    
    def evaluateDistanceToGoal(self, node):
        goalStateNode = findNodeByValue(createGoalNodeSet(), node.value)
        if goalStateNode == None:
            return 0
        distance = node.distanceTo(goalStateNode)
        return distance

    
    def getNeighborNode(self, node, direction):
        x = node.posX
        y = node.posY

        if direction == Direction.UP:
            y -= 1
        elif direction == Direction.DOWN:
            y += 1
        elif direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.LEFT:
            x -= 1
        n = findNodeByCoordinates(self.nodes, x, y)
        if n == None or n.value == BLACK_SPACE:
            return None
        return n

    def nextStates(self):
        ws = findWhitespaceNode(self.nodes)
        states = []
        for d in Direction:
            neighbor = self.getNeighborNode(ws, d)
            if neighbor == None:
                continue
            s = self.nextState(neighbor)
            if s == None:
                continue
            states.append(s)
        return states

    def __str__(self):
        self.nodes.sort(key = lambda x: (x.posY, x.posX))
        oldY = 0
        string = ""
        for n in self.nodes:
            isSingleSpace = False
            if oldY < n.posY:
                string += "\n"
                oldY = n.posY
            if n.value == WHITE_SPACE:
                string += "W"
            elif n.value == BLACK_SPACE:
                string += "X"
            else:
                if n.value >= 10:
                    isSingleSpace = True
                string += str(n.value) 
            
            string += "  "
            if not isSingleSpace: 
                string += " "
        string += "\n\n\n"
        return string
    def __lt__(self, other):
        return 0

class Puzzle:
    def __init__(self):
        pass
    
    def solve(self):
        node = self.a_star()
        if node != "ERROR":
            path = []
            while node != None:
                path.insert(0, node)
                node = node.predecessor
            print("-------------\n%d steps taken to achieve solution:" % (len(path)))
            for n in path:
                print(n)
        else:
            print("Failed to find solution.")

    def a_star(self):
        print("Beginning A* Search:")
        nodes = self.createInitialNodeSet()
        start = State(0, None, nodes)

        openQ = PriorityQueue()
        closedQ = PriorityQueue() 

        state_counter = 0

        openQ.put((0, start))
        start.enqueued = Enqueued.OPEN
        while not openQ.empty():
            state_counter += 1
            currentState = openQ.get()[1]
            print("State #%d Visited" % (state_counter))
            print(currentState)
            closedQ.put(currentState)
            currentState.enqueued = Enqueued.CLOSED
            if currentState.h() == 0: # check goal state:
                return currentState
            states = currentState.nextStates() 
            for successor in states:
                if successor.enqueued == Enqueued.NOT_QUEUED:
                    openQ.put((successor.h(), successor))
                    successor.enqueued = Enqueued.OPEN
                else:
                    newDistance = self.evaluateDistanceToGoal(successor)
                    if newDistance < successor.g:
                        successor.g = newDistance
        return "ERROR"
    


    def createInitialNodeSet(self):
        nodes = []
        nodes.append(Node(2, 0, 0))
        nodes.append(Node(3, 1, 0))
        nodes.append(Node(7, 2, 0))
        nodes.append(Node(4, 3, 0))
        nodes.append(Node(5, 4, 0))

        nodes.append(Node(1, 0, 1))
        nodes.append(Node(BLACK_SPACE, 1, 1))
        nodes.append(Node(11, 2, 1))
        nodes.append(Node(BLACK_SPACE, 3, 1))
        nodes.append(Node(8, 4, 1))

        nodes.append(Node(6, 0, 2))
        nodes.append(Node(10, 1, 2))
        nodes.append(Node(WHITE_SPACE, 2, 2))
        nodes.append(Node(12, 3, 2))
        nodes.append(Node(15, 4, 2))

        nodes.append(Node(9, 0, 3))
        nodes.append(Node(BLACK_SPACE, 1, 3))
        nodes.append(Node(14, 2, 3))
        nodes.append(Node(BLACK_SPACE, 3, 3))
        nodes.append(Node(20, 4, 3))

        nodes.append(Node(13, 0, 4))
        nodes.append(Node(16, 1, 4))
        nodes.append(Node(17, 2, 4))
        nodes.append(Node(18, 3, 4))
        nodes.append(Node(19, 4, 4))

        return nodes

def createGoalNodeSet():
    nodes = []
    nodes.append(Node(1, 0, 0))
    nodes.append(Node(2, 1, 0))
    nodes.append(Node(3, 2, 0))
    nodes.append(Node(4, 3, 0))
    nodes.append(Node(5, 4, 0))

    nodes.append(Node(6, 0, 1))
    nodes.append(Node(BLACK_SPACE, 1, 1))
    nodes.append(Node(7, 2, 1))
    nodes.append(Node(BLACK_SPACE, 3, 1))
    nodes.append(Node(8, 4, 1))

    nodes.append(Node(9, 0, 2))
    nodes.append(Node(10, 1, 2))
    nodes.append(Node(WHITE_SPACE, 2, 2))
    nodes.append(Node(11, 3, 2))
    nodes.append(Node(12, 4, 2))

    nodes.append(Node(13, 0, 3))
    nodes.append(Node(BLACK_SPACE, 1, 3))
    nodes.append(Node(14, 2, 3))
    nodes.append(Node(BLACK_SPACE, 3, 3))
    nodes.append(Node(15, 4, 3))

    nodes.append(Node(16, 0, 4))
    nodes.append(Node(17, 1, 4))
    nodes.append(Node(18, 2, 4))
    nodes.append(Node(19, 3, 4))
    nodes.append(Node(20, 4, 4))

    return nodes



pz = Puzzle()
pz.solve()