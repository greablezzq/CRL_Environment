from ClassCraftStructure import *

def RabbitStew():
    planks = craftItem("planks", True, ['spruce', 'birch', 'dark_oak'])
    coal = craftItem("coal")
    rabbit = craftItem("rabbit")
    carrot = craftItem("carrot")
    potato = craftItem("potato")
    brown_mushroom = craftItem("brown_mushroom")
    cooked_rabbit = craftItem("cooked_rabbit", origin=False)
    baked_potato = craftItem("baked_potato", origin=False)
    bowl = craftItem("bowl", origin=False)
    rabbit_stew = craftItem("rabbit_stew", origin=False)
    recipe = craftStructure()
    recipe.addRecipe(cooked_rabbit, {rabbit:1, coal:1})
    recipe.addRecipe(baked_potato, {potato:1, coal:1})
    recipe.addRecipe(bowl, {planks:3})
    recipe.addRecipe(rabbit_stew, {cooked_rabbit:1, carrot:1, baked_potato:1,brown_mushroom:1, bowl:1})
    return recipe.getOriginalRecipe(rabbit_stew, 1)