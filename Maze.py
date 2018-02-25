import random

'''
Char representation to print the maze and make difference between walls and path cells
'''
WALL_CHAR = "1"
PATH_CHAR = "0"

'''
Maze class allowing the program to generate a random new maze
'''


class Maze:
    '''
    Constructor for the Maze class
    @brief Create the maze object and initialize the visual and logical matrices
    @param width    The needed width for the maze
    @param height   The needed width for the maze
    '''

    def __init__(self, width, height):
        self.width = width + 1  # Y
        self.height = height + 1  # X
        self.matrix = self.generateEmpty()
        self.visual_matrix = self.generateEmptyVisual()

    '''
    Function generating a maze by applying a depth-first recursive backtracker algorithm
    '''

    def generate(self):
        coordX = 0
        coordY = 0

        # Starting in the top left corner of the matrix
        path = [(coordX, coordY)]
        self.matrix[coordX][coordY].visited = True
        visitedCount = 1
        visitedCells = list()

        # Continue until there is unvisited cells
        while (visitedCount < self.height * self.width):
            currentNeighbours = self.findCurrentNeighbours(coordX, coordY)  # Get neighbours cells of the current one
            self.removeRandomWall(coordX, coordY)  # remove random wall around the current cell

            if (currentNeighbours is not None):
                visitedCells.append((coordX, coordY))  # mark this position as visited
                nextCoordX, nextCoordY = random.choice(currentNeighbours)  # choose a random neighboor cell in the list

                # break walls between the current cell and the next one to create a path
                self.matrix[coordX][coordY].removeWalls(nextCoordX, nextCoordY)
                self.matrix[nextCoordX][nextCoordY].removeWalls(coordX, coordY)

                self.matrix[nextCoordX][nextCoordY].visited = True

                # Move to the next cell and add it to the path
                coordX = nextCoordX
                coordY = nextCoordY
                path.append((coordX, coordY))
                visitedCount += 1

            # If there isn't any neighbour for a given cell, then go back to the last one
            elif (len(visitedCells) > 0):
                coordX, coordY = visitedCells.pop()
                path.append((coordX, coordY))

        # When everything is done, reset the cells as unvisited
        for i in range(self.height):
            for j in range(self.width):
                self.matrix[i][j].visited = False

    '''
    Function filling the logical matrix with empty cells (ie with walls on each direction)
    '''

    def generateEmpty(self):
        matrix = []
        for x in range(self.height):
            new = []
            for y in range(self.width):
                new.append(Cell.Cell(x, y))
            matrix.append(new)
        return matrix

    '''
    Function filling the visual matrix with walls only
    '''

    def generateEmptyVisual(self):
        matrix = []
        for x in range(self.height * 2 + 1):
            new = []
            for y in range(self.width * 2 + 1):
                new.append(WALL_CHAR)
            matrix.append(new)
        return matrix

    '''
    Function removing a wall on a random direction of a given cell
    @param coordX   The X position of the cell
    @param coordY   The Y position of the cell
    '''

    def removeRandomWall(self, coordX, coordY):
        wallsList = self._findCurrentWalls(coordX, coordY)  # Get the position of the walls for this cell
        toRemoveX, toRemoveY = random.choice(wallsList)  # Choose a random tuple in the walls list

        # Check that we are not removing a one of the border walls
        if (toRemoveY > 0 and toRemoveY < self.width * 2 and toRemoveX > 0 and toRemoveX < self.height * 2):
            if (random.randint(0,
                               10) > 7):  # Remove the wall only with a chance of 3/10 to avoid massive hole in the maze
                self.visual_matrix[toRemoveX][toRemoveY] = PATH_CHAR

    '''
    Helper function to get a cell's walls coordinates as a list of tuples
    @param coordX   The X position of the cell
    @param coordY   The Y position of the cell
    '''

    def _findCurrentWalls(self, coordX, coordY):
        wallsList = []
        wallsList.append((coordX * 2, coordY * 2 + 1))
        wallsList.append((coordX * 2 + 1, coordY * 2 + 2))
        wallsList.append((coordX * 2 + 2, coordY * 2 + 1))
        wallsList.append((coordX * 2 + 1, coordY * 2))
        return wallsList

    '''
    Function finding all the neighbour cells of a given cell
    @param coordX   The X position of the cell
    @param coordY   The Y position of the cell
    '''

    def findCurrentNeighbours(self, coordX, coordY):
        neighboursList = list()
        self._findCurrentNeighbours(neighboursList, coordX - 1, coordY)  # Top
        self._findCurrentNeighbours(neighboursList, coordX, coordY + 1)  # Right
        self._findCurrentNeighbours(neighboursList, coordX + 1, coordY)  # Bottom
        self._findCurrentNeighbours(neighboursList, coordX, coordY - 1)  # Left

        if (len(neighboursList) > 0):
            return neighboursList
        else:
            return None

    '''
    Helper function to check if we are not out of the matrix and the neighbour is unvisited
    @param neighboursList   The cells list to check
    @param coordX   The X position of the current cell
    @param coordY   The Y position of the current cell
    '''

    def _findCurrentNeighbours(self, neighboursList, coordX, coordY):
        if (coordY >= 0 and coordY < self.width and coordX >= 0 and coordX < self.height and not self.matrix[coordX][
            coordY].visited):
            neighboursList.append((coordX, coordY))

    '''
    Based on the logical maatrix generated by the algorithm, update the visual matrix used to display the maze
    '''

    def updateVisualMatrix(self):
        for x in range(self.height):
            for y in range(self.width):
                self.visual_matrix[x * 2 + 1][y * 2 + 1] = PATH_CHAR

                if (not self.matrix[x][y].walls["TOP"]):
                    self.visual_matrix[x * 2][y * 2 + 1] = PATH_CHAR
                if (not self.matrix[x][y].walls["RIGHT"]):
                    self.visual_matrix[x * 2 + 1][y * 2 + 2] = PATH_CHAR
                if (not self.matrix[x][y].walls["BOTTOM"]):
                    self.visual_matrix[x * 2 + 2][y * 2 + 1] = PATH_CHAR
                if (not self.matrix[x][y].walls["LEFT"]):
                    self.visual_matrix[x * 2 + 1][y * 2] = PATH_CHAR

    '''
    Override the str() function to be able to print the maze easily
    '''

    def __str__(self):
        self.updateVisualMatrix()
        res = str(self.width * 2 + 1) + "\n"
        for x in range(self.height * 2 + 1):
            for y in range(self.width * 2 + 1):
                res += self.visual_matrix[x][y] + " "
            res += "\n"
        return res

    '''
    Function printing the maze in a text file
    '''

    def toFile(self, mazeInText):
        f = open('maze.txt', 'w')
        f.write(mazeInText)
        f.close()
