import ClassTask
import generateTaskAndRewards
# RewardForTouchingBlockType
# RewardForCollectingItem
# RewardForDamagingEntity

class taskRewards:
    def __init__(self,  isMergedReward = False) -> None:
        self.taskList=[]
        self.isMergedReward=isMergedReward

    def taskEncoding(self):
        for i in range(len(self.taskList)):
            self.taskList[i].index = 2**(i)

    def taskDecoding(self, encodedReward):
        binReward = bin(encodedReward)
        realReward = [0 for _ in self.taskList]
        for i in range(len(self.taskList)):
            if(binReward[-(i+1)] == 'b'):
                break
            realReward[i] = int(binReward[-(i+1)])
        if(self.isMergedReward):
            mergedReward = 0
            for i in range(len(self.taskList)):
                if (realReward[i]==1):
                    mergedReward += self.taskList[i].reward
            return mergedReward 
        else:
            return realReward

    def generateRewardString(self):
        rewardForTouchingBlockType = []
        rewardForCollectingItem = []
        rewardForDamagingEntity = []
        rewardForDiscardingItem = []
        for i in self.taskList:
            if i.type=='c':
                rewardForCollectingItem.append(i.generateRewardString())
            elif i.type=='t':
                rewardForTouchingBlockType.append(i.generateRewardString())
            elif i.type=='d':
                rewardForDamagingEntity.append(i.generateRewardString())
            elif i.type=='di':
                rewardForDiscardingItem.append(i.generateRewardString())
        if rewardForTouchingBlockType:
            rewardForTouchingBlockType = ['<RewardForTouchingBlockType>'] + rewardForTouchingBlockType + ['</RewardForTouchingBlockType>']
        if rewardForCollectingItem:
            rewardForCollectingItem = ['<RewardForCollectingItem>'] + rewardForCollectingItem + ['</RewardForCollectingItem>']
        if rewardForDamagingEntity:
            rewardForDamagingEntity = ['<RewardForDamagingEntity>'] + rewardForDamagingEntity + ['</RewardForDamagingEntity>']
        if rewardForDiscardingItem:
            rewardForDiscardingItem = ['<RewardForDiscardingItem>'] + rewardForDiscardingItem + ['</RewardForDiscardingItem>']
        rewardList = rewardForTouchingBlockType + rewardForCollectingItem + rewardForDamagingEntity+rewardForDiscardingItem
        return rewardList

# t = taskRewards()
# t.taskList = generateTaskAndRewards.generateTasks()
# t.taskEncoding()
# rewardlist = t.generateRewardString()
# for i in rewardlist:
#     print(i)