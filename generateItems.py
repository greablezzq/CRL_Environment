from typing import Dict
from ClassCraftStructure import *
import craftTasks
import random

def MergeItemDictionary(dictionaryList):
    mergedItemDictionary = {}
    for dict in dictionaryList:
        for item in dict.keys():
            if item in mergedItemDictionary:
                mergedItemDictionary[item] = mergedItemDictionary[item] + dict[item]
            else:
                mergedItemDictionary[item] = dict[item]
    return mergedItemDictionary

def ItemStringGenerator(x,y,z,item:craftItem,variantIndex=None):
    if item.variantBool:
        try:
            variant = item.variant[variantIndex]
        except:
            variant = random.choice(item.variant)
        return '<DrawItem x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}" variant="{0[4]}"/>'.format([x,y,z,item.name,variant])
    else:
        return '<DrawItem x="{0[0]}"  y="{0[1]}" z="{0[2]}" type="{0[3]}"/>'.format([x,y,z,item.name])
        

def ItemsStringGenerator(xRange, y, zRange, itemsDictionary:Dict):
    itemsString=[]
    space = [[i,j] for i in xRange for j in zRange]
    k = sum(itemsDictionary.values())
    positions = random.choices(space, k=k)
    for item in itemsDictionary.keys():
        for _ in range(itemsDictionary[item]):
            position = positions.pop()
            itemsString.append(ItemStringGenerator(position[0], y, position[1], item))
    return itemsString

