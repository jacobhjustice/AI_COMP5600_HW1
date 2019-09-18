NUM_QUEENS = 25

class Queen:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def equals(self, testQueen):
        return self.posX == testQueen.posX and self.posY == testQueen.posY

    def __str__(self):
        return str(self.posX) + "," + str(self.posY) 
    
    def score(self, queenMap):
        i = 0
        
        # Vertical Check
        for x in range(NUM_QUEENS):
            queenInRange = queenMap.map[x][self.posY]
            if queenInRange != None and queenInRange != self:
                i += 1

        # Horizontal Check
        for y in range(NUM_QUEENS):
            queenInRange = queenMap.map[self.posX][y]
            if queenInRange != None and queenInRange != self:
                i += 1


        # Front Diagonal Check
        startY = self.posY - self.posX
        for index in range(0,NUM_QUEENS - startY):
            if index < 0 or startY + index < 0 or index >= NUM_QUEENS or index + startY >= NUM_QUEENS:
                continue
            queenInRange = queenMap.map[index][startY + index]
            if queenInRange != None and queenInRange != self:
                i += 1
            
        # Back Diagonal Check
        startY = self.posY + self.posX
        for index in range(startY):
            if startY - index < 0 or index < 0 or index >= NUM_QUEENS  or startY - index >= NUM_QUEENS:
                continue
            queenInRange = queenMap.map[index][startY - index]
            if queenInRange != None and queenInRange != self:
                i += 1
        return i
        
class QueenMap: 
    def __init__(self):
        self.queens = []
        self.map = []
        for x in range(NUM_QUEENS):
            arr = []
            for y in range(NUM_QUEENS):
                arr.append(None)
            self.map.append(arr)

    def addQueen(self, queen):
        self.map[queen.posX][queen.posY] = queen
        self.queens.append(queen)
    
    def moveQueen(self, oldPosX, oldPosY, newPosX, newPosY):
        # Retrieve the queen from the board mapping, and remove it from that spot in the map
        q = self.map[oldPosX][oldPosY]
        self.map[oldPosX][oldPosY] = None

        # Update the queen to the new position and insert back into the map
        q.posX = newPosX
        q.posY = newPosY
        self.map[newPosX][newPosY] = q

    # Checks to see if there is a better place vertically to move the queen that will result in a lower score
    def adjustQueen(self, queen):
        currentScore = NUM_QUEENS + 1
        oldY = queen.posY
        newY = oldY
        for y in range(NUM_QUEENS):
            queen.posY = y
            tempScore = queen.score(qm)
            if tempScore < currentScore:
                newY = y
                currentScore = tempScore
        self.moveQueen(queen.posX, oldY, queen.posX, newY)

    
    def printQueens(self):
        intersecting = 0
        for i in range(NUM_QUEENS):
            q = self.queens[i]
            # print(q)
            score = q.score(self)
            if score > 0:
                intersecting += 1
                if score > 1:
                    print("ERROR: SHOULD NOT INTERSECT WITH MORE THAN ONE.")
        print(str(intersecting) + " total intersecting nodes")
        string = ""
        for x in self.map:
            for y in x:
                string += "_" if y == None else "Q"
                string += "\t"
            string += "\n"
        print(string)
    
    def optimizeQueens(self):
        for queen in self.queens[1:]:
            self.adjustQueen(queen)

qm = QueenMap()

# Create NUM_QUEENS queens, and populate in the map
for i in range(NUM_QUEENS):
    q = Queen(i, 0)
    qm.addQueen(q)


qm.optimizeQueens()
qm.optimizeQueens()


qm.printQueens()