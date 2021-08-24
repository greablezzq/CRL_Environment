from typing import Dict
import random
from past.utils import old_div

def generateEntity(x,y,z,type):
    return '<DrawEntity x="{0[0]}" y="{0[1]}" z="{0[2]}" type="{0[3]}" />'.format([x,y,z,type])

def generateEntities(xRange,y,zRange, typesDictionary:Dict):
    entitiesString = []
    space = [[i,j] for i in xRange for j in zRange]
    k = sum(typesDictionary.values())
    positions = random.choices(space, k=k)
    for entity in typesDictionary.keys():
        for _ in range(typesDictionary[entity]):
            position = positions.pop()
            entitiesString.append(generateEntity(position[0],y,position[1],entity))

    return entitiesString

# copy from malmo source code begin
def getCorner(index,top,left,expand=0,y=0, ARENA_WIDTH = 20, ARENA_BREADTH = 20):
    ''' Return part of the XML string that defines the requested corner'''
    x = str(-(expand+old_div(ARENA_WIDTH,2))) if left else str(expand+old_div(ARENA_WIDTH,2))
    z = str(-(expand+old_div(ARENA_BREADTH,2))) if top else str(expand+old_div(ARENA_BREADTH,2))
    return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'

# copy from malmo souce code end
