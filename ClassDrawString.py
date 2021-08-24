import generateMaze
import StructureGrid
import random
from past.utils import old_div
import generateItems
import ClassCraftStructure
import craftTasks
import numpy as np

# copy from Malmo source code
def GenCuboid(x1, y1, z1, x2, y2, z2, blocktype):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="' + blocktype + '"/>'

def GenCuboidWithVariant(x1, y1, z1, x2, y2, z2, blocktype, variant):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="' + blocktype + '" variant="' + variant + '"/>'
# copy end

class drawString():
    def __init__(self,xRange, yRange, zRange) -> None:
        self.xMin = xRange[0]
        self.xMax = xRange[1]
        self.yMin = yRange[0]
        self.yMax = yRange[1]
        self.zMin = zRange[0]
        self.zMax = zRange[1]
        self.beautifulPlaceNum = 2
        self.mazeNumberBasic = 3
        self.mazeNumberCom = 3
        self.lakeNumBasic = 2
        self.lakeNumberCom = 2
        self.saplingNum = 100
        self.treeNum = 50
        self.mazeSizeRange = [4,7]
        self.craftTaskRange = [4,6]
        self.lakeSizeRange = [3,8]
        self.craftTask = [craftTasks.RabbitStew]
        self.craftTaskRepeat = 2
        self.drawList=[]
        self.mountainSize = [6,12]
        self.mountainNum = 3
        self.maps = [[StructureGrid.grid() for _ in range(self.zMax - self.zMin+1)] for _ in range(self.xMax - self.xMin+1)]
        self.animalSpawner = ['Rabbit', 'Sheep', 'Chicken']
        self.animals=['Rabbit', 'Sheep', 'Chicken', 'Pig', 'Villager']
        self.animalsAmount=[30,30,30,30,5]
        self.plants=['potatoes', 'carrots'] 
        self.plantsAmount = [30,30]
        self.mushroomNum = 30
        pass

    def GenerateSpace(self):
        self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="air" />'.format([self.xMin, self.yMin, self.zMin, self.xMax, self.yMax, self.zMax]))

    def GenerateGround(self):
        self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="grass" />'.format([self.xMin, self.yMin-1, self.zMin, self.xMax, self.yMin-1, self.zMax]))

    def GenerateBoundary(self, height = 5, position=[]):
        if not position:
            position = [int((self.xMax+self.xMin)/2), int((self.xMax+self.xMin)/2), self.zMin, self.zMax]
        print('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="dirt" />'.format([position[0], self.yMin, position[2], position[1], self.yMin+height, position[3]]))
        self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="dirt" />'.format([position[0], self.yMin, position[2], position[1], self.yMin+height, position[3]]))
        self.UpdateMap(position, 'boundary')

    def AssignSubparts(self):
        self.GenerateSpace()
        self.GenerateGround()
        self.GenerateBoundary()
        self.GenerateBasicPart()
        self.GenerateComprehensivePart()
        for _ in range(self.saplingNum):
            self.AddSaplings()
        for _ in range(self.treeNum):
            self.AddTrees()
        pass

    def UpdateMap(self, inf, type):
        xMin = int((self.xMax+self.xMin)/2)
        if(type == 'maze'):
            startPosition = inf[0]
            x,y,z=startPosition[0],startPosition[1],startPosition[2]
            maze = inf[1]
            for h in range(len(maze)):
                for w in range(len(maze[0])):
                    if(maze[h][w]==1):
                        self.maps[x+h-self.xMin][z+w-self.zMin].add = False
                    else:
                        self.maps[x+h-self.xMin][z+w-self.zMin].height = 1
                        self.maps[x+h-self.xMin][z+w-self.zMin].add = True
        if(type == 'boundary'):
            for x in range(inf[0]-self.xMin, inf[1]-self.xMin+1):
                for z in range(inf[2]-self.zMin, inf[3]-self.zMin+1):
                    self.maps[x][z].add = False
                    self.maps[x][z].function.append(type)
        if(type == 'beautifulPlace'):
            for x in range(inf[0] - self.xMin, inf[0]+27-self.xMin):
                for z in range(inf[1] - self.zMin, inf[1]+27-self.zMin):
                    self.maps[x][z].add = False
                    self.maps[x][z].function.append(type)
        if(type == 'craft'):
            for x in inf[0]:
                for z in inf[1]:
                    self.maps[x-self.xMin][z-self.zMin].add = False
                    self.maps[x-self.xMin][z-self.zMin].function.append(type)
        if(type == 'lake'):
            for x in (inf[0], inf[0]+inf[2][0]):
                for z in (inf[1], inf[1]+inf[2][1]):
                    self.maps[x][z].add = False
                    self.maps[x][z].function.append(type)
        if(type == 'goldPlace'):
            for x in range(inf[0] - self.xMin, inf[0]+27-self.xMin):
                for z in range(inf[1] - self.zMin, inf[1]+27-self.zMin):
                    self.maps[x][z].add = False
                    self.maps[x][z].function.append(type)
        if(type == 'lakeCom'):
            for x in (inf[0]+xMin-self.xMin, inf[0]+inf[2][0]+xMin-self.xMin):
                for z in (inf[1], inf[1]+inf[2][1]):
                    self.maps[x][z].add = False
                    self.maps[x][z].function.append('lake')

        pass

    def GenerateMaze(self, startPosition, height, width, deleteRatio=0, startType=[], endType=[], borderType=[], pathType=[], obstacleType=[], obstacleSize = 2, lava=False):
        maze = generateMaze.MazeStringGenerate(startPosition, height, width, deleteRatio, startType, endType, borderType, pathType, obstacleType, obstacleSize, lava)
        self.drawList += maze[0]
        self.UpdateMap([startPosition, maze[1]],'maze')

    def GenerateCraftRegion(self, position, size, itemsDictionary):
        region = [position[0]+self.xMin, self.yMin, position[1]+self.zMin, position[0]+self.xMin+size[0], self.yMin, position[1]+self.zMin+size[1]]
        self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="red_flower" />'.format(region))
        print('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="red_flower" />'.format(region))
        xRange = range(position[0]+self.xMin, position[0]+self.xMin+size[0])
        zRange = range(position[1]+self.zMin, position[1]+self.zMin+size[1])
        self.drawList += generateItems.ItemsStringGenerator(xRange,self.yMin+1,zRange,itemsDictionary())
        self.UpdateMap([xRange, zRange], 'craft')

    def GenerateBasicPart(self):
        MAX_TRY = 50
        success = True

        for _ in range(MAX_TRY):
            map = [[0 for  _ in range(self.zMax - self.zMin+1)] for _ in range(int((self.xMax+self.xMin)/2) - self.xMin)]
            mazePosition = []
            mazeSize= [] 
            beautifulPosition = []
            craftPosition = []
            craftSize = []
            # Place Beautiful Place
            for i in range(self.beautifulPlaceNum):
                placementResult = self.Placement(map, [27, 27])
                beautifulPosition.append([placementResult[0], placementResult[1]])
                map = placementResult[2]
            # Place Maze
            for i in range(self.mazeNumberBasic):
                regionSize = [random.randint(self.mazeSizeRange[0], self.mazeSizeRange[1]), random.randint(self.mazeSizeRange[0], self.mazeSizeRange[1])]
                placementResult = self.Placement(map, [regionSize[0]*2+1, regionSize[1]*2+1])
                if placementResult:
                    mazePosition.append([placementResult[0], placementResult[1]])
                    mazeSize.append(regionSize)
                    map = placementResult[2]
                else:
                    success = False
                    break
            # Place craft items
            for i in range(len(self.craftTask)):
                position = []
                size = []
                for j in range(self.craftTaskRepeat):
                    regionSize = [random.randint(self.craftTaskRange[0], self.craftTaskRange[1]), random.randint(self.craftTaskRange[0], self.craftTaskRange[1])]
                    placementResult = self.Placement(map, [regionSize[0], regionSize[1]])
                    if placementResult:
                        position.append([placementResult[0], placementResult[1]])
                        size.append(regionSize)
                        map = placementResult[2]
                    else:
                        success = False
                        break
                craftPosition.append(position)
                craftSize.append(size)

            if(success):
                for i in range(self.beautifulPlaceNum):
                    if(i==0):
                        self.AddBeautifulPlace([beautifulPosition[0][0]+self.xMin,beautifulPosition[0][1]+self.zMin],'diamond_pickaxe')
                    else:
                        self.AddBeautifulPlace([beautifulPosition[i][0]+self.xMin,beautifulPosition[i][1]+self.zMin],'gold_ingot')
                
                for i in range(self.mazeNumberBasic):
                    self.GenerateMaze([mazePosition[i][0]+self.xMin, self.yMin, mazePosition[i][1]+self.zMin],mazeSize[i][0],mazeSize[i][1],0.5*random.random(),lava=random.randint(0,1))
                
                for i in range(len(craftPosition)):
                    for j in range(self.craftTaskRepeat):
                        self.GenerateCraftRegion(craftPosition[i][j], craftSize[i][j], self.craftTask[i])

                for i in range(self.lakeNumBasic):
                    map = self.AddLakes(map)
                print(beautifulPosition)
                print(mazePosition)
                print(craftPosition)
                return

        print('Error!')


    def GenerateComprehensivePart(self):
        xMin = int((self.xMax+self.xMin)/2)
        
        MAX_TRY = 50
        success = True
        
            # Place Gold Place
        for _ in range(MAX_TRY):
            map = [[0 for  _ in range(self.zMax - self.zMin+1)] for _ in range(self.xMax - xMin)]
            goldPlacePosition =[]
            for i in range(len(self.animalSpawner)):
                placementResult = self.Placement(map, [27, 27])
                # print(bool(placementResult))
                if(placementResult):
                    goldPlacePosition.append([placementResult[0], placementResult[1]])
                    map = placementResult[2]
                else:
                    success = False
                    break
            if(success):
                for i in range(len(self.animalSpawner)):
                    self.AddGoldPlace([goldPlacePosition[i][0]+xMin, goldPlacePosition[i][1]+self.zMin], self.animalSpawner[i])
                for i in range(self.lakeNumberCom):
                    map = self.AddLakes(map,False)
                for i in range(self.mountainNum):
                    self.AddMountain()
                for i in range(len(self.animals)):
                    for _ in range(self.animalsAmount[i]):
                        self.AddAnimal(self.animals[i])
                for i in range(len(self.plants)):
                    for _ in range(self.plantsAmount[i]):
                        self.AddPlants(self.plants[i])
                for i in range(self.mushroomNum):
                    self.AddMushroom()
                return

    def AddSaplings(self):
        while(True):
            x = random.randint(0,self.xMax - self.xMin)
            z = random.randint(0,self.zMax - self.zMin)
            if(self.maps[x][z].add):
                position = [x+self.xMin, self.maps[x][z].height + self.yMin, z+self.zMin]
                self.drawList.append('<DrawBlock x="{0[0]}" y="{0[1]}" z="{0[2]}" type="sapling"/>'.format(position))
                self.maps[x][z].add = False
                self.maps[x][z].function.append('sapling')
                return

    def AddTrees(self):
        while(True):
            x = random.randint(1,self.xMax - self.xMin - 1)
            z = random.randint(1,self.zMax - self.zMin - 1)
            varients = ['spruce', 'birch', 'dark_oak']
            checkPosition = True
            for i in [x-1,x,x+1]:
                for j in [z-1,z,z+1]:
                    checkPosition = checkPosition and self.maps[i][j].add
                    checkPosition = checkPosition and (self.maps[i][j].height<self.maps[x][z].height+3)
            if(checkPosition):
                varient = varients[random.randint(0,len(varients)-1)]
                treePosition = [x+self.xMin, self.maps[x][z].height+self.yMin, z+self.zMin, x+self.xMin, self.maps[x][z].height+self.yMin+2, z+self.zMin, varient]
                leavesPosition = [x+self.xMin - 1, self.maps[x][z].height+self.yMin+3, z+self.zMin - 1, x+self.xMin + 1, self.maps[x][z].height+self.yMin+3, z+self.zMin + 1]
                
                self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="planks" variant="{0[6]}"/>'.format(treePosition))
                self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="leaves" />'.format(leavesPosition))
                for i in [x-1,x,x+1]:
                    for j in [z-1,z,z+1]:
                        self.maps[i][j].add = False
                        self.maps[x][z].function.append('tree')
                return

    def AddMountain(self):

        def GetMountain(sizeX, sizeZ):
            mountain = [[0 for _ in range(sizeZ)] for _ in range(sizeX)]
            for _ in range(int(2.5*sizeX*sizeZ)):
                randomX = random.gauss(0.5, 0.25)
                randomZ = random.gauss(0.5, 0.25)
                if(randomX>0 and randomX<1 and randomZ>0 and randomZ<1):
                    mountain[int(randomX*sizeX)][int(randomZ*sizeZ)]+=1
            min = np.min(np.array(mountain))
            for i in range(sizeX):
                for j in range(sizeZ):
                    mountain[i][j] -= min
            return mountain

        xMin = int((self.xMax+self.xMin)/2)
        while(True):
            sizeX = random.randint(self.mountainSize[0], self.mountainSize[1])
            sizeZ = random.randint(self.mountainSize[0], self.mountainSize[1])
            pX = random.randint(xMin-self.xMin, self.xMax - self.xMin - sizeX)
            pZ = random.randint(1, self.zMax - self.zMin -sizeZ)
            checkPosition = True
            for i in range(sizeX):
                for j in range(sizeZ):
                    checkPosition = checkPosition and self.maps[pX+i][pZ+j].add and not self.maps[pX+i][pZ+j].function
            if(checkPosition):
                mountain = GetMountain(sizeX, sizeZ)
                for i in range(sizeX):
                    for j in range(sizeZ):
                        self.maps[pX+i][pZ+j].height += mountain[i][j]
                        self.maps[pX+i][pZ+j].function.append('mountain')
                        position = [pX+i+self.xMin, self.yMin, pZ+j+self.zMin, pX+i+self.xMin, self.yMin+mountain[i][j], pZ+j+self.zMin]
                        self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="grass" />'.format(position))
                return

    def Placement(self, map, regionSize):
        MAX_TRY = 50
        for _ in range(MAX_TRY):
            x = int(random.random()*(len(map)-regionSize[0]))
            y = int(random.random()*(len(map[0])-regionSize[1]))
            subregion = [i[y:y+regionSize[1]] for i in map[x:x+regionSize[0]]]
            if (sum([sum(i) for i in subregion])==0):
                for l in range(x,x+regionSize[0]):
                    for m in range(y,y+regionSize[1]):
                        map[l][m] = 1
                return [x,y,map]

        return []

    def AddLakes(self, map, basic = True):
        MAX_TRY = 50
        for _ in range(MAX_TRY):
            regionSize = [random.randint(self.lakeSizeRange[0], self.lakeSizeRange[1]), random.randint(self.lakeSizeRange[0], self.lakeSizeRange[1])]
            placementResult = self.Placement(map, regionSize)
            if basic:               
                if placementResult:
                    print('add lake {0[0]}, {0[1]}'.format([placementResult[0]+self.xMin, placementResult[1]+self.zMin]))
                    region = [placementResult[0]+self.xMin, self.yMin - 3, placementResult[1]+self.zMin, placementResult[0]+self.xMin+regionSize[0], self.yMin - 1, placementResult[1]+self.zMin+regionSize[1]]
                    self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="water" />'.format(region))
                    self.UpdateMap([placementResult[0],placementResult[1],regionSize],'lake')
                    return placementResult[2]
            else:
                xMin = int((self.xMax+self.xMin)/2)
                if placementResult:
                    print('add lake {0[0]}, {0[1]}'.format([placementResult[0]+xMin, placementResult[1]+self.zMin]))
                    region = [placementResult[0]+xMin, self.yMin - 3, placementResult[1]+self.zMin, placementResult[0]+xMin+regionSize[0], self.yMin - 1, placementResult[1]+self.zMin+regionSize[1]]
                    self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="water" />'.format(region))
                    self.UpdateMap([placementResult[0],placementResult[1],regionSize],'lakeCom')
                    return placementResult[2]

    def AddAnimal(self, animal):
        while(True):
            x = random.randint(int((self.xMax+self.xMin)/2)+1, self.zMax - self.zMin)
            z = random.randint(0, self.zMax - self.zMin)
            if(self.maps[x][z].add):
                inf=[x+self.xMin, self.maps[x][z].height+self.yMin, z+self.zMin, animal]
                self.drawList.append('<DrawEntity x="{0[0]}" y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format(inf))
                self.maps[x][z].add = False
                self.maps[x][z].function.append(animal)
                return

    def AddPlants(self, plant):
        while(True):
            x = random.randint(int((self.xMax+self.xMin)/2)+1, self.zMax - self.zMin)
            z = random.randint(0, self.zMax - self.zMin)
            if(self.maps[x][z].add):
                inf=[x+self.xMin, self.maps[x][z].height+self.yMin, z+self.zMin, plant]
                infGround=[x+self.xMin, self.maps[x][z].height+self.yMin-1, z+self.zMin, 'dirt']
                self.drawList.append('<DrawBlock x="{0[0]}" y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format(inf))
                self.drawList.append('<DrawBlock x="{0[0]}" y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format(infGround))
                self.maps[x][z].add = False
                self.maps[x][z].function.append(plant)
                return

    def AddMushroom(self):
        while(True):
            x = random.randint(int((self.xMax+self.xMin)/2)+1, self.zMax - self.zMin)
            z = random.randint(0, self.zMax - self.zMin)
            if(self.maps[x][z].add):
                infGround = [x+self.xMin, self.maps[x][z].height+self.yMin-1, z+self.zMin, 'dirt']
                inf=[x+self.xMin, self.maps[x][z].height+self.yMin, z+self.zMin, x+self.xMin, self.maps[x][z].height+self.yMin+2, z+self.zMin]
                self.drawList.append('<DrawBlock x="{0[0]}" y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format(infGround))
                self.drawList.append('<DrawCuboid x1="{0[0]}" y1="{0[1]}" z1="{0[2]}" x2="{0[3]}" y2="{0[4]}" z2="{0[5]}" type="brown_mushroom_block"/>'.format(inf))
                self.maps[x][z].add = False
                self.maps[x][z].function.append('brown_mushroom')
                return

    def AddBeautifulPlace(self, Position, reward=''):
        # copy from Malmo source code
        def Menger(xorg, yorg, zorg, size = 27, blocktype = "stone", variant ="smooth_granite", holetype="air"):
            #draw solid chunk
            genstring = GenCuboidWithVariant(xorg,yorg,zorg,xorg+size-1,yorg+size-1,zorg+size-1,blocktype,variant) + "\n"
            #now remove holes
            unit = size
            while (unit >= 3):
                w=old_div(unit,3)
                for i in range(0, size, unit):
                    for j in range(0, size, unit):
                        x=xorg+i
                        y=yorg+j
                        genstring += GenCuboid(x+w,y+w,zorg,(x+2*w)-1,(y+2*w)-1,zorg+size-1,holetype) + "\n"
                        y=yorg+i
                        z=zorg+j
                        genstring += GenCuboid(xorg,y+w,z+w,xorg+size-1, (y+2*w)-1,(z+2*w)-1,holetype) + "\n"
                        genstring += GenCuboid(x+w,yorg,z+w,(x+2*w)-1,yorg+size-1,(z+2*w)-1,holetype) + "\n"
                unit = w
            genstring += GenCuboid(xorg,yorg,zorg+12,xorg+size-1,yorg+2,zorg+14,holetype) + "\n"
            genstring += GenCuboid(xorg+11,yorg-1,zorg+11,xorg+15,yorg-1,zorg+15,"flowing_water") + "\n"
            genstring += GenCuboid(xorg+12,yorg-1,zorg+12,xorg+14,yorg-1,zorg+14,"obsidian") + "\n"
            genstring += '<DrawBlock x="{0[0]}" y="{0[1]}" z="{0[2]}" type="diamond_block"/>'.format([xorg+13,yorg-1,zorg+13]) + "\n"
            item = ClassCraftStructure.craftItem(reward)
            genstring += generateItems.ItemStringGenerator(xorg+13,yorg,zorg+13,item)
            return genstring
        # copy end

        self.drawList += Menger(Position[0], self.yMin, Position[1])
        self.UpdateMap(Position, 'beautifulPlace')

    def AddGoldPlace(self, Position, animal=''):
        # copy from Malmo source code
        def Menger(xorg, yorg, zorg, size = 27, blocktype = "gold_block",  holetype="air"):
            #draw solid chunk
            genstring = GenCuboid(xorg,yorg,zorg,xorg+size-1,yorg+size-1,zorg+size-1,blocktype) + "\n"
            #now remove holes
            unit = size
            while (unit >= 3):
                w=old_div(unit,3)
                for i in range(0, size, unit):
                    for j in range(0, size, unit):
                        x=xorg+i
                        y=yorg+j
                        genstring += GenCuboid(x+w,y+w,zorg,(x+2*w)-1,(y+2*w)-1,zorg+size-1,holetype) + "\n"
                        y=yorg+i
                        z=zorg+j
                        genstring += GenCuboid(xorg,y+w,z+w,xorg+size-1, (y+2*w)-1,(z+2*w)-1,holetype) + "\n"
                        genstring += GenCuboid(x+w,yorg,z+w,(x+2*w)-1,yorg+size-1,(z+2*w)-1,holetype) + "\n"
                unit = w
            genstring += GenCuboid(xorg+11,yorg-1,zorg+11,xorg+15,yorg-1,zorg+15,"grass") + "\n"
            genstring += GenCuboid(xorg+12,yorg-1,zorg+12,xorg+14,yorg-1,zorg+14,"grass") + "\n"
            genstring += '<DrawBlock x="{0[0]}" y="{0[1]}" z="{0[2]}" type="mob_spawner" variant="{0[3]}"/>'.format([xorg+13,yorg,zorg+13,animal]) + "\n"
            return genstring
        # copy end

        self.drawList += Menger(Position[0], self.yMin, Position[1])
        self.UpdateMap(Position, 'goldPlace')

    def PrintMapsAdd(self):
        for x in range(len(self.maps)):
            # a = 
            print(' '.join([str(int(self.maps[x][y].add)) for y in range(len(self.maps[0]))]))

# myDrawString = drawString([-40,40],[40,60],[-40,40])
# myDrawString.AssignSubparts()
# myDrawString.PrintMapsAdd()
# print('---------------------------')
# myDrawString.PrintMapsAdd()
# for i in myDrawString.drawList:
#     print(i)
# print(int(myDrawString.maps[0][0].add))