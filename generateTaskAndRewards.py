import ClassTask
def generateTasks():
    taskList = []
    collectItem = ['planks','coal','rabbit','carrot','potato','brown_mushroom','cooked_rabbit','baked_potato','bowl','rabbit_stew','stick','gold_ingot','golden_pickaxe','dirt']
    collectItemReward = [10,10,10,10,10,10,20,20,20,30,20,10,30,5]
    touchingBlockType = ['diamond_block', 'water', 'flowing_water', 'lava']
    touchingBlockTypeReward = [10, -10, -10, -100]
    damagingEntity = ['Rabbit', 'Sheep', 'Chicken', 'Pig', 'Villager']
    damagingEntityReward = [40, 20, 20, -5, -20]
    for i in range(len(collectItem)):
        taskList.append(ClassTask.task('collect_'+collectItem[i], 'c', collectItem[i], reward=collectItemReward[i]))
        taskList.append(ClassTask.task('discard_'+collectItem[i], 'di', collectItem[i], reward=-collectItemReward[i]))
    for i in range(len(touchingBlockType)):
        taskList.append(ClassTask.task('touch_'+touchingBlockType[i], 't', [touchingBlockType[i], 'oncePerTimeSpan'], reward=touchingBlockTypeReward[i]))
    for i in range(len(damagingEntity)):
        taskList.append(ClassTask.task('damage_'+damagingEntity[i], 'd', damagingEntity[i], reward=damagingEntityReward[i]))
    return taskList