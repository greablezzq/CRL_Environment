import random
class task:
    def __init__(self, name, type, inf, scale = 0.2, reward = 0) -> None:
        self.name = name
        self.initialReward = reward
        self.reward = reward
        # 'c':'collect', 't':'touchBlockType', 'd':'DamagingEntity', 'di':DiscardingItem
        self.type = type
        self.scale = scale
        self.index = -1
        self.inf = inf

    def updateReward(self):
        r = (random.random()-0.5)/0.5*self.scale*self.initialReward
        self.reward += r

    def generateRewardString(self):
        if(self.type == 'c'):
            return '<Item reward="{0[0]}" type="{0[1]}"/>'.format([self.index, self.inf])
        if(self.type == 't'):
            return '<Block reward="{0[0]}" type="{0[1]}" behaviour="{0[2]}"/>'.format([self.index, self.inf[0], self.inf[1]])
        if(self.type == 'd'):
            return '<Mob type="{0[0]}" reward="{0[1]}"/>'.format([self.inf, self.index])
        if(self.type == 'di'):
            return '<Item reward="{0[0]}" type="{0[1]}"/>'.format([self.index, self.inf])
        return ''
    
    def __str__(self) -> str:
        return 'name:'+self.name+' reward:'+self.reward+' type'+self.type

    def __repr__(self) -> str:
        return 'name:'+self.name+' reward:'+self.reward+' type'+self.type