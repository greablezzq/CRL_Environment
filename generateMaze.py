from ClassMazeGenerator import mazeGenerator
import random

def MazeStringGenerate(startPosition, height, width, deleteRatio=0, startType=[], endType=[], borderType=[], pathType=[], obstacleType=[], obstacleSize = 2, lava=False, reward='gold_ingot'):
    x,y,z=startPosition[0],startPosition[1],startPosition[2]
    mazeString=[]
    mazeGenerator1 = mazeGenerator(height, width, deleteRatio) 
    mazeGenerator1.GenerateMaze()
    mazeGenerator1.deleteRandomObstacle()
    mazeGenerator1.SetEntry()
    mazeGenerator1.setAimPosition()
    # for line in mazeGenerator1.maze:
    #     print(line)

    if not startType:
        startType = ["cobblestone"]
    if not endType:
        endType = ["lapis_block"]
    if not borderType:
        borderType = ["grass", "dirt", "cobblestone", "sandstone"]
    if not pathType:
        pathType = ["grass", "dirt", "cobblestone", "sandstone"]
    if not obstacleType:
        obstacleType = ["grass", "dirt", "cobblestone", "sandstone"]

    if lava:
        for h in range(1, mazeGenerator1.totalHeight-1):
                for w in range(1, mazeGenerator1.totalWidth-1):
                    if(mazeGenerator1.maze[h][w]==1):
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="lava" />'.format([x+h,y-1,z+w]))
                    elif(mazeGenerator1.maze[h][w]==0):
                        type0=random.choice(pathType)
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y,z+w, type0]))
                    elif(mazeGenerator1.maze[h][w]==2):
                        type2=random.choice(startType)
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y,z+w, type2]))
                    elif(mazeGenerator1.maze[h][w]==3):
                        type3=random.choice(endType)
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y,z+w, type3]))
                        mazeString.append('<DrawItem x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y+1,z+w, reward]))
        for h in [0,mazeGenerator1.totalHeight-1]:
            for w in range(mazeGenerator1.totalWidth):
                if(mazeGenerator1.maze[h][w]==1):
                    type1=random.choice(borderType)
                    mazeString.append('<DrawCuboid x1="{0[0]}"  y1="{0[1]}" z1="{0[2]}" x2="{0[0]}"  y2="{0[3]}" z2="{0[2]}" type="{0[4]}" />'.format([x+h,y,z+w,y+2,type1]))
                elif(mazeGenerator1.maze[h][w]==2):
                        type2=random.choice(startType)
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y,z+w, type2]))
        for h in range(1, mazeGenerator1.totalHeight-1):
            for w in [0, mazeGenerator1.totalWidth-1]:
                if(mazeGenerator1.maze[h][w]==1):
                    type1=random.choice(borderType)
                    mazeString.append('<DrawCuboid x1="{0[0]}"  y1="{0[1]}" z1="{0[2]}" x2="{0[0]}"  y2="{0[3]}" z2="{0[2]}" type="{0[4]}" />'.format([x+h,y,z+w,y+2,type1]))
                elif(mazeGenerator1.maze[h][w]==2):
                        type2=random.choice(startType)
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y,z+w, type2]))

    else:
        for h in range(mazeGenerator1.totalHeight):
                for w in range(mazeGenerator1.totalWidth):
                    if(mazeGenerator1.maze[h][w]==1):
                        type1=random.choice(obstacleType)
                        mazeString.append('<DrawCuboid x1="{0[0]}"  y1="{0[1]}" z1="{0[2]}" x2="{0[0]}"  y2="{0[3]}" z2="{0[2]}" type="{0[4]}" />'.format([x+h,y,z+w,y+obstacleSize,type1]))
                    elif(mazeGenerator1.maze[h][w]==0):
                        type0=random.choice(pathType)
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y,z+w, type0]))
                    elif(mazeGenerator1.maze[h][w]==2):
                        type2=random.choice(startType)
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y,z+w, type2]))
                    elif(mazeGenerator1.maze[h][w]==3):
                        type3=random.choice(endType)
                        mazeString.append('<DrawBlock x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y,z+w, type3]))
                        mazeString.append('<DrawItem x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x+h,y+1,z+w, reward]))
    
    return [mazeString, mazeGenerator1.maze]

# mazestring = MazeStringGenerate([0,46,0],4,6,lava=False)
# for i in mazestring:
#     print(i)