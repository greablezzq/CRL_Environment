from past.utils import old_div
import generateMaze
import generateItems
import craftTasks
import ClassCraftStructure
import ClassDrawString
import ClassTaskRewards
import generateTaskAndRewards


class generateMissionXml:
    def __init__(self, taskRewards):
        self.summary = 'hello!'
        # whether the time changes in the game
        self.allowPassageOfTime = False
        # check https://www.chunkbase.com/apps/superflat-generator#3;7,2*3,2;1;village
        self.generateType='flatGenerate'
        self.generateString = "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"
        # start time
        self.startTime = 12000
        # weather
        self.weather = 'clear'
        # Max time(ms), 0 means no reqiurement
        self.serverQuitFromTimeUp = 100000
        # Server Quit When Any Agent Finishes
        self.serverQuitWhenAnyAgentFinishes = True
        # Name
        self.name = 'mybot'
        # Agent placement(x,y,z,yaw)
        self.agentPlacement=[-50, 50.0, -50, 90]
        # Inventory
        self.inventory={0:'diamond_pickaxe'}
        # observations
        self.observationFromGrid=''
        self.observationFromVideo=True
        self.videoWidth = 432
        self.videoHeight = 240
        # mode
        self.mode = 'Survival'
        self.myDrawString = ClassDrawString.drawString([-70,70],[46,500],[-70,70])
        self.myDrawString.GenerateSpace()
        self.myDrawString.AssignSubparts()
        self.taskAndRewards = taskRewards



    def getSummary(self):
        return '<Summary>{}</Summary>'.format(self.summary)

    def getName(self):
        return '<Name>{}</Name>'.format(self.name)

    def getServerQuitFromTimeUp(self):
        if(self.serverQuitFromTimeUp == 0):
            return ''
        else:
            return '<ServerQuitFromTimeUp timeLimitMs="{}"/>'.format(str(self.serverQuitFromTimeUp))

    def getServerQuitWhenAnyAgentFinishes(self):
        if(self.serverQuitWhenAnyAgentFinishes):
            return '<ServerQuitWhenAnyAgentFinishes/>'
        else:
            return ''

    def getWeather(self):
        return '<Weather>{}</Weather>'.format(self.weather)

    def getStartTime(self):
        return '<StartTime>{}</StartTime>'.format(str(self.startTime))

    def getAllowPassageOfTime(self):
        if(self.allowPassageOfTime):
            return '<AllowPassageOfTime>true</AllowPassageOfTime>'
        else:
            return '<AllowPassageOfTime>false</AllowPassageOfTime>'

    def getGenerator(self):
        return {
            'flatGenerate':'<FlatWorldGenerator generatorString="{}"/>'.format(self.generateString)
        }[self.generateType]
    
    def getAgentPlacement(self):
        if self.agentPlacement:
            l = [str(i) for i in self.agentPlacement]
            return '<Placement x="{0[0]}" y="{0[1]}" z="{0[2]}" yaw="{0[3]}"/>'.format(l)
        else:
            return ''

    def addInventory(self, slot, item):
        self.inventory[slot] = item

    def getInventory(self):
        if self.inventory:
            inventoryList=['<Inventory>']+['<InventoryItem slot="{0[0]}" type="{0[1]}"/>'.format([str(key), value]) for key,value in self.inventory.items()]+['</Inventory>']
            return ''.join(inventoryList)
        else:
            return ''

    def setObservationFromGrid(self, name="floor3x3", min=[-1,-1,-1], max=[1,1,1]):
        gridName='<Grid name="{}">'.format(name)
        gridMin='<min x="{0[0]}" y="{0[1]}" z="{0[2]}"/>'.format([str(i) for i in min])
        gridMax='<max x="{0[0]}" y="{0[1]}" z="{0[2]}"/>'.format([str(i) for i in max])
        self.observationFromGrid = ''.join(['<ObservationFromGrid>',gridName,gridMin,gridMax,'</Grid>','</ObservationFromGrid>'])
    
    def setObservationFromVideo(self):
        if self.observationFromVideo:
            return '''<VideoProducer want_depth="true">
                <Width>''' + str(self.videoWidth) + '''</Width>
                <Height>''' + str(self.videoHeight) + '''</Height>
            </VideoProducer>'''
        else:
            return ''

    def draw(self):
        drawList = []
        drawList += self.myDrawString.drawList
        return ''.join(drawList)


    def drawAnimation(self):
        pass

    def rewardList(self):
        return ''.join(self.taskAndRewards.generateRewardString())

    def GenerateXML(self):
        missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                '''+self.getSummary()+'''
              </About>
              
            <ServerSection>
              <ServerInitialConditions>
              <AllowSpawning>true</AllowSpawning>
              <AllowedMobs>Pig Sheep Chicken Rabbit</AllowedMobs>
                <Time>'''+self.getStartTime()+self.getAllowPassageOfTime()+'''  
                </Time>'''+self.getWeather()+'''
              </ServerInitialConditions>
              <ServerHandlers>'''+self.getGenerator()+'''
                  <DrawingDecorator>
                    ''' + self.draw()+'''
                  </DrawingDecorator>'''+self.getServerQuitFromTimeUp()+self.getServerQuitWhenAnyAgentFinishes()+'''
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="'''+self.mode+'''">'''+self.getName()+'''
                <AgentStart>'''+self.getAgentPlacement()+self.getInventory()+'''
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>'''+self.observationFromGrid+self.setObservationFromVideo()+self.rewardList()+'''
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                  <SimpleCraftCommands/>
                  <InventoryCommands/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''
        return missionXML

def WriteXMLToFile(XML):
    pass

def ReadXMLFromFile(path):
    pass