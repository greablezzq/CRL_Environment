class craftItem:
    def __init__(self, name, variantBool = False, variant=[], origin=True):
        self.name = name
        self.variantBool = variantBool
        self.variant = variant
        self.origin = origin
    
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

class craftStructure:
    def __init__(self):
        self.recipeDictionary = {}

    def addRecipe(self, target, materials):
        self.recipeDictionary[target] = materials

    def getRecipe(self, target):
        return self.recipeDictionary[target]

    def getOriginalRecipe(self, target, amount):
        originalRecipe = {}
        for item in self.recipeDictionary[target].keys():
            if item.origin:
                if item in originalRecipe:
                    originalRecipe[item] = originalRecipe[item] + self.recipeDictionary[target][item]
                else:
                    originalRecipe[item] = self.recipeDictionary[target][item]
            else:
                subRecipe = self.getOriginalRecipe(item, self.recipeDictionary[target][item])
                for subitem in subRecipe.keys():
                    if subitem in originalRecipe:
                        originalRecipe[subitem] = originalRecipe[subitem] + subRecipe[subitem]
                    else:
                        originalRecipe[subitem] = subRecipe[subitem]
        
        updateOriginalRecipe = {}
        for item in originalRecipe.keys():
            updateOriginalRecipe[item] = originalRecipe[item] * amount
        
        return updateOriginalRecipe