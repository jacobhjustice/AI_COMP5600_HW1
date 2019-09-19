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

WHITE_SPACE = -5
BLACK_SPACE = -666

class Node:
    def __init__(self, value, posX, posY):
        self.value = value
        self.posX = posX
        self.posY = posY
        self.fromNode = None
        self.enqueued = Enqueued.NOT_QUEUED
        self.g = -1
        self.h = -1

    def f(self):
        return self.g + self.h

    def attachPreviousNode(node):
        self.fromNode = node

    def __str__(self):
        return str(self.value) + " ----- " + str(self.posX) + "," + str(self.posY)

    def distanceTo(self, node):
        return abs(self.posX - node.posX) + abs(self.posY - node.posY)

    def swapNodes(self, node):
        tempX = node.posX
        tempY = node.posY

        node.posX = self.posX
        node.posY = self.posY

        self.posX = tempX
        self.posY = tempY

class Puzzle:
    def __init__(self):
        self.nodes = self.createInitialNodeSet()
        
    
    def a_star(self):
        start = self.findWhitespaceNode()
        start.g = 0
        openQ = PriorityQueue()
        closedQ = PriorityQueue() 
        openQ.put((0, start))
        start.enqueued = Enqueued.OPEN
        while not openQ.empty():
            n = openQ.get()
            closedQ.put(n)
            if self.heuristic() == 0: # check goal state:
                return "SUCCESS!!!"
            neighbors = self.getNeighbors(n)
            for successor in neighbors:
                if successor.enqueued == Enqueued.NOT_QUEUED:
                    cost = n.distanceTo(successor)
                    successor.g = n.g + cost
                    successor.h = self.testSwap(n, successor)

                    openQ.put((self.evaluateDistanceToGoal(successor), successor))
                    successor.enqueued = Enqueued.OPEN
                    successor.attachPreviousNode(n)
                else:
                    newDistance = self.evaluateDistanceToGoal(successor)
                    if newDistance < successor.g:
                        successor.g = newDistance
        return "ERROR"

    def testSwap(self, currentNode, neighbor):
        currentNode.swapNodes(neighbor)
        d = self.heuristic()
        currentNode.swapNodes(neighbor)
        return d
    def heuristic(self):
        d = 0
        for n in nodes:
            d += n.evaluateDistanceToGoal()
        return d

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

    def createGoalNodeSet(self):
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

    def findNodeByValue(self, value, nodes):

        self.nodes.sort(key = lambda x: x.value)

        # Add 5 to value for 1 white space and 4 black spaces
        # subtract 1 from value for index offset
        index = value + 5 - 1
        return self.nodes[index]

    def findWhitespaceNode(self):
        self.nodes.sort(key = lambda x: x.value)
        return self.nodes[0]
    
    def findNodeByCoordinates(self, x, y):
        if x < 0 or y < 0 or x > 4 or y > 4:
            return None
        self.nodes.sort(key = lambda x: (x.posX, x.posY))
        index = x * 5 + y
        node = self.nodes[index]
        if node.value == BLACK_SPACE:
            return None
        return node

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
        return self.findNodeByCoordinates(x, y)

    def getNeighbors(self, node):
        neighbors = []
        distances = []
        for d in Direction:
            neighbor = self.getNeighborNode(node, d)
            if neighbor == None:
                continue
            neighbors.append(neighbor)
        return neighbors

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
        return string

    def evaluateDistanceToGoal(self, node):
        goal = self.createGoalNodeSet()
        nodeGoalState = self.findNodeByValue(node.value, goal)
        distance = node.distanceTo(nodeGoalState)
        return distance

pz = Puzzle()
n = pz.findWhitespaceNode()
print(pz)
# print(n)
# print(pz.getNeighborNode(n, Direction.UP))
# print(pz.getNeighborNode(n, Direction.DOWN))
# print(pz.getNeighborNode(n, Direction.LEFT))
# print(pz.getNeighborNode(n, Direction.RIGHT))
# print(pz.getNeighborsSortedLowestHeuristic(n)) 