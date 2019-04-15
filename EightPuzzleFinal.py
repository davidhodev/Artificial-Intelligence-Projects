import math
from queue import PriorityQueue

# DAVID HO DH2487
#Creating a Node class to store each 8 puzzle node
class Node:
    def __init__(self, data, goal, path, fValueListString, linearListString, move=""):
        self.data = data
        self.goal = goal
        self.fValue = self.manhattanDistance(goal) + (len(path)/2)
        self.path = path + move
        self.fValueListString = fValueListString + str(int(self.fValue)) + ' '
        self.linearConflict = self.linearConflictRow(goal) + self.linearConflictCol(goal)
        #self.linearConflict = self.manhattanDistance(goal) + (2*(self.linearConflictRow(goal) + self.linearConflictCol(goal)))
        self.linearListString = linearListString + str(int(self.fValue) + (2*self.linearConflict)) + ' '

    # Copies the matrix of the node (deep copy)
    def copyMatrix(self):
        copy = []
        for row in range(len(self.data)):
            rowCopy = []
            for col in range(len(self.data)):
                rowCopy.append(self.data[row][col])
            copy.append(rowCopy)
        return copy

    #Function to check if done.
    def checkGoal(self, goal):
        for row in range(len(self.data)):
            for col in range(len(self.data)):
                if (self.data[row][col] != goal.data[row][col]):
                    return False
        return True

    # Returns a dictionary of every coordinate
    def dictMatrix(self):
        dict = {}
        for row in range(3):
            for col in range(3):
                dict[self.data[row][col]] = (row, col)
        return dict

    #Function that calculates the heuristic function of Manhattan distances
    def manhattanDistance(self, goalMatrix):
        # H(x) set to 0
        hx = 0
        dict = {}
        for row in range(len(self.data)):
            for col in range(len(self.data)):
                dict[goalMatrix[row][col]] = (row, col)
        for row in range(len(self.data)):
            for col in range(len(self.data)):
                if (self.data[row][col] != 0):
                    goalX,goalY = dict[self.data[row][col]]
                    hx += int(math.fabs(goalX-row) + math.fabs(goalY-col))
        # print("HX: ", hx)
        return hx

    # Calculate Linear Conflicts
    def linearConflictRow(self, goalMatrix):
        lc = 0
        for row in range(len(self.data)):
            count = 0
            conflictList = []
            for col in range(len(self.data)):
                if (self.data[row][col] in goalMatrix[row]):
                    conflictList.append(self.data[row][col])
                    count += 1
            # Two of the same in the same Row
            if count == 2:
                first = self.data[row].index(conflictList[0])
                second = self.data[row].index(conflictList[1])
                firstGoal = goalMatrix[row].index(conflictList[0])
                secondGoal = goalMatrix[row].index(conflictList[1])
                if (firstGoal - secondGoal > 0 and first - second < 0):
                    lc += 1
                if (firstGoal - secondGoal < 0 and first - second > 0):
                    lc += 1
            if count == 3:
                first = self.data[row].index(conflictList[0])
                second = self.data[row].index(conflictList[1])
                third = self.data[row].index(conflictList[2])
                firstGoal = goalMatrix[row].index(conflictList[0])
                secondGoal = goalMatrix[row].index(conflictList[1])
                thirdGoal = goalMatrix[row].index(conflictList[2])
                if (firstGoal - secondGoal > 0 and first - second < 0):
                    lc += 1
                if (firstGoal - secondGoal < 0 and first - second > 0):
                    lc += 1
                if (firstGoal - thirdGoal > 0 and first - third < 0):
                    lc += 1
                if (firstGoal - thirdGoal < 0 and first - third > 0):
                    lc += 1
                if (secondGoal - thirdGoal > 0 and second - third < 0):
                    lc += 1
                if (secondGoal - thirdGoal < 0 and second - third > 0):
                    lc += 1
        return lc
    #Linear Conflits for Columnn
    def linearConflictCol(self, goalMatrix):
        # Switch Rows and Cols for both node matrix and goal Matrix
        inverseRow1 = [self.data[0][0],self.data[1][0],self.data[2][0]]
        inverseRow2 = [self.data[0][1],self.data[1][1],self.data[2][1]]
        inverseRow3 = [self.data[0][2],self.data[1][2],self.data[2][2]]
        inverseMatrix = [inverseRow1, inverseRow2, inverseRow3]

        inverseGoalRow1 = [goalMatrix[0][0],goalMatrix[1][0],goalMatrix[2][0]]
        inverseGoalRow2 = [goalMatrix[0][1],goalMatrix[1][1],goalMatrix[2][1]]
        inverseGoalRow3 = [goalMatrix[0][2],goalMatrix[1][2],goalMatrix[2][2]]
        inverseGoalMatrix = [inverseGoalRow1, inverseGoalRow2, inverseGoalRow3]

        lc = 0
        for row in range(len(inverseMatrix)):
            count = 0
            conflictList = []
            for col in range(len(inverseMatrix)):
                if (inverseMatrix[row][col] in inverseGoalMatrix[row]):
                    conflictList.append(inverseMatrix[row][col])
                    count += 1
            # Two of the same in the same Row
            if count == 2:
                first = inverseMatrix[row].index(conflictList[0])
                second = inverseMatrix[row].index(conflictList[1])
                firstGoal = inverseGoalMatrix[row].index(conflictList[0])
                secondGoal = inverseGoalMatrix[row].index(conflictList[1])
                if (firstGoal - secondGoal > 0 and first - second < 0):
                    lc += 1
                if (firstGoal - secondGoal < 0 and first - second > 0):
                    lc += 1
            if count == 3:
                first = inverseMatrix[row].index(conflictList[0])
                second = inverseMatrix[row].index(conflictList[1])
                third = inverseMatrix[row].index(conflictList[2])
                firstGoal = inverseGoalMatrix[row].index(conflictList[0])
                secondGoal = inverseGoalMatrix[row].index(conflictList[1])
                thirdGoal = inverseGoalMatrix[row].index(conflictList[2])
                if (firstGoal - secondGoal > 0 and first - second < 0):
                    lc += 1
                if (firstGoal - secondGoal < 0 and first - second > 0):
                    lc += 1
                if (firstGoal - thirdGoal > 0 and first - third < 0):
                    lc += 1
                if (firstGoal - thirdGoal < 0 and first - third > 0):
                    lc += 1
                if (secondGoal - thirdGoal > 0 and second - third < 0):
                    lc += 1
                if (secondGoal - thirdGoal < 0 and second - third > 0):
                    lc += 1
        return lc



#Creates tuples in order for it to be hashable
def hashMatrix(state):
    listerine = ()
    for row in state:
        for col in row:
            listerine += (col,)
    return listerine

#Generates the list of all possible children nodes
def moves(node):
	#All possible moves
	allMoves = [[['R ','D '],['L ','R ','D '],['L ','D ']],
                [['R ','U ','D '],['L ','R ','U ','D '],['L ','U ','D ']],
                [['R ','U '],['L ','R ','U '],['L ','U ']]]
	#Location in blank position
	zeroX, zeroY = node.dictMatrix()[0]
	allMovesList = []
	for direction in allMoves[zeroX][zeroY]:
		childNode = node.copyMatrix()
		#Left
		if (direction == 'L '):
			childNode[zeroX][zeroY], childNode[zeroX][zeroY-1] = childNode[zeroX][zeroY-1], childNode[zeroX][zeroY]
			allMovesList.append((childNode, 'L '))
		#Right
		if (direction == 'R '):
			childNode[zeroX][zeroY], childNode[zeroX][zeroY+1] = childNode[zeroX][zeroY+1], childNode[zeroX][zeroY]
			allMovesList.append((childNode, 'R '))
		#Up
		if (direction == 'U '):
			childNode[zeroX][zeroY], childNode[zeroX-1][zeroY] = childNode[zeroX-1][zeroY], childNode[zeroX][zeroY]
			allMovesList.append((childNode, 'U '))
		#Down
		if (direction == 'D '):
			childNode[zeroX][zeroY], childNode[zeroX+1][zeroY] = childNode[zeroX+1][zeroY], childNode[zeroX][zeroY]
			allMovesList.append((childNode, 'D '))
	return allMovesList


#Uses Manhattan Distance to set frontier set, and number of Nodes
def manhattanSolve(startMatrix, goalMatrix, writingFile):
    startNode = Node(startMatrix, goalMatrix, '', '', "")
    goalNode = Node(goalMatrix, goalMatrix, '', '', "")

    #Initial state put into frontier
    frontier = [startNode]
    finalList = set()
    numOfNodes = 1
    fValueString = ''

    while True:
        #Sort the frontier based on fValue
        frontier.sort(key = lambda x:x.fValue,reverse=False)
        currentNode = frontier.pop(0)
        if (currentNode.checkGoal(goalNode)):
            # Writes Depth of the Path
            writingFile.write(str(int(len(currentNode.path)/2)))
            writingFile.write('\n')
            # Writes Total Number of Nodes
            writingFile.write(str(numOfNodes))
            writingFile.write('\n')
            # Writes Path
            writingFile.write(currentNode.path)
            writingFile.write('\n')
            print(int(len(currentNode.path)/2))
            print(numOfNodes)
            print(currentNode.path)
            preAdditionList = list(map(int , currentNode.fValueListString.split()))
            finalFValueString = ''
            for i in range(1,len(preAdditionList)):
                preAdditionList[i] += 1
                preAdditionList[i] = str(preAdditionList[i])
            for i in preAdditionList:
                finalFValueString += str(i) + ' '
            print(finalFValueString)
            # Writes F Values
            writingFile.write(finalFValueString)
            break
        finalList.add(hashMatrix(currentNode.data))
        nextSequence = moves(currentNode)
        for child in nextSequence:
            successor = Node(child[0], goalMatrix, currentNode.path, currentNode.fValueListString, currentNode.linearListString, child[1])
            if successor not in frontier and hashMatrix(successor.data) not in finalList:
                numOfNodes += 1
                frontier.append(successor)

#Uses Manhattan Distance to set frontier set, and number of Nodes
def LinearConflictSolve(startMatrix, goalMatrix, writingFile):
    startNode = Node(startMatrix, goalMatrix, '', '', "")
    goalNode = Node(goalMatrix, goalMatrix, '', '', "")
    #Initial state put into frontier
    frontier = [startNode]
    finalList = set()
    numOfNodes = 1
    fValueString = ''

    while True:
        #Sort the frontier based on LinearConflict + hX
        frontier.sort(key = lambda x:((x.fValue) + (2*x.linearConflict)),reverse=False)
        currentNode = frontier.pop(0)
        if (currentNode.checkGoal(goalNode)):
            # Writes Depth of the Path
            writingFile.write(str(int(len(currentNode.path)/2)))
            writingFile.write('\n')
            # Writes Total Number of Nodes
            writingFile.write(str(numOfNodes))
            writingFile.write('\n')
            # Writes Path
            writingFile.write(currentNode.path)
            writingFile.write('\n')
            print(int(len(currentNode.path)/2))
            print(numOfNodes)
            print(currentNode.path)
            preAdditionList = list(map(int , currentNode.linearListString.split()))
            finalFValueString = ''
            for i in range(1,len(preAdditionList)):
                preAdditionList[i] += 1
                preAdditionList[i] = str(preAdditionList[i])
            for i in preAdditionList:
                finalFValueString += str(i) + ' '
            print(finalFValueString)
            # Writes F Values
            writingFile.write(finalFValueString)
            break
        finalList.add(hashMatrix(currentNode.data))
        nextSequence = moves(currentNode)
        for child in nextSequence:
            successor = Node(child[0], goalMatrix, currentNode.path, currentNode.fValueListString, currentNode.linearListString, child[1])
            if successor not in frontier and hashMatrix(successor.data) not in finalList:
                numOfNodes += 1
                frontier.append(successor)


class Puzzle:
    def __init__(self,filename):
        self.filename = filename

    def solve(self):
        matrixToUse = []
        with open(self.filename) as file:
            for line in file:
                rowMatrixToUse = []
                line = line.replace(' ', "")
                line = line.replace('\n', "")
                for character in line:
                    rowMatrixToUse.append(int(character))
                matrixToUse.append(rowMatrixToUse)

        startMatrix = matrixToUse[0:3]
        goalMatrix = matrixToUse[4:7]

        #Prints startMatrix and goalMatrix
        printList = [startMatrix, goalMatrix]

        #Makes outputFil for A
        outputFileName = self.filename[0:-4] + '_A.txt'
        writingFile = open(outputFileName, "w")

        # Makes output File for B
        outputFileBName = self.filename[0:-4] + '_B.txt'
        writingBFile = open(outputFileBName, "w")


        for i in printList:
            for row in range(len(startMatrix)):
                for col in range(len(startMatrix)):
                    number = str(i[row][col]) + ' '
                    writingFile.write(number)
                    writingBFile.write(number)
                    print(i[row][col], end = ' ')
                print()
                writingFile.write('\n')
                writingBFile.write('\n')
            print()
            writingFile.write('\n')
            writingBFile.write('\n')

        print("MANHATTAN DISTANCE: ")
        manhattanSolve(startMatrix, goalMatrix, writingFile)

        print("LINEAR CONFLICTS: ")
        LinearConflictSolve(startMatrix, goalMatrix, writingBFile)
        file.close()

# Put in input file here!
puz = Puzzle('Input4.txt')
puz.solve()
