import random

class mazeGenerator:
    def __init__(self, height, width, deleteRatio=0):
        self.height = height
        self.width = width
        self.totalHeight = 2 * self.height + 1
        self.totalWidth = 2 * self.width + 1
        self.unvisited = []
        self.visited = []
        self.maze=[]
        self.deleteRatio = deleteRatio
        self.maxObstacleNumber = 0

    def InitialMaze(self):
        self.unvisited = []
        self.visited = []
        self.maze=[[1 for x in range(self.totalWidth)] for y in range(self.totalHeight)]
        for h in range(self.totalHeight):
            for w in range(self.totalWidth):
                if(h%2 and w%2):
                    self.maze[h][w] = 0
                    self.unvisited.append([h,w])
        return self.maze

    def NextPossiblePosition(self, currentPosition):
        x, y = currentPosition[0], currentPosition[1]
        nextPossiblePosition = [[x+2,y],[x-2,y],[x,y+2],[x,y-2]]
        nextPositions=[]
        for i in nextPossiblePosition:
            if not (i[0]==self.totalHeight or i[0]<0 or i[1]==self.totalWidth or i[1]<0 or i not in self.unvisited):
                nextPositions.append(i)
        return nextPositions

    def GenerateMaze(self):
        self.InitialMaze()
        currentPosition = [1,1]
        self.visited.append(currentPosition)
        self.unvisited.remove(currentPosition)
        while True:
            if not self.unvisited:
                break
            else:
                nextPossiblePositions = self.NextPossiblePosition(currentPosition)
                if not nextPossiblePositions:
                    currentPosition = random.choice(self.visited)
                    continue
                else:
                    nextPosition = random.choice(nextPossiblePositions)
                    self.maze[(currentPosition[0] + nextPosition[0]) // 2][(currentPosition[1] + nextPosition[1]) // 2] = 0
                    self.visited.append(nextPosition)
                    self.unvisited.remove(nextPosition)
                    currentPosition = nextPosition
        self.maxObstacleNumber = sum([sum(i) for i in self.maze]) - (self.totalWidth + self.totalHeight - 1) * 2
        return self.maze

    def SetEntry(self, number=3):
        setNumber = 0
        while setNumber<number:
            side = random.randint(0,3)
            if(side == 0):
                position = random.randint(1, self.totalWidth-1)
                if(self.maze[1][position] == 0):
                    setNumber += 1
                    self.maze[0][position] = 2
                else:
                    continue
            if(side == 1):
                position = random.randint(1, self.totalHeight-1)
                if(self.maze[position][1] == 0):
                    setNumber += 1
                    self.maze[position][0] = 2
                else:
                    continue
            if(side == 2):
                position = random.randint(1, self.totalWidth-1)
                if(self.maze[self.totalHeight-1][position] == 0):
                    setNumber += 1
                    self.maze[self.totalHeight][position] = 2
                else:
                    continue
            if(side == 1):
                position = random.randint(1, self.totalHeight-1)
                if(self.maze[position][self.totalWidth-1] == 0):
                    setNumber += 1
                    self.maze[position][self.totalWidth] = 2
                else:
                    continue
        return self.maze

    def setAimPosition(self):
        while True:
            h = random.randint(1, self.totalHeight - 2)
            w = random.randint(1, self.totalWidth - 2)
            if self.maze[h][w] == 0:
                self.maze[h][w] = 3
                return
            else:
                continue

    def deleteRandomObstacle(self):
        number = 0
        requireNumber = int(self.deleteRatio*self.maxObstacleNumber)
        while number<requireNumber:
            h = random.randint(1, self.totalHeight - 2)
            w = random.randint(1, self.totalWidth - 2)
            if self.maze[h][w] == 1:
                self.maze[h][w] = 0
                number+=1
                # print('delete'+str(h)+'  '+str(w))
        return
