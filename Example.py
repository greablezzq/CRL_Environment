from __future__ import print_function
from __future__ import division
from builtins import range
import MalmoPython
from past.utils import old_div
import os
import sys
import time
import generateMissionXML
import ClassTaskRewards
import json
import generateTaskAndRewards

def agentPolicy(worldState, reward):
    return []


if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)



taskAndRewards = ClassTaskRewards.taskRewards()
taskAndRewards.taskList = generateTaskAndRewards.generateTasks()
taskAndRewards.taskEncoding()

missionXMLGenerator = generateMissionXML.generateMissionXml(taskAndRewards)
missionXMLGenerator.serverQuitFromTimeUp = 150000
missionXMLGenerator.generateString="3;7,220*1,5*3,2;3;,biome_1"
missionXMLGenerator.agentPlacement=[10, 47.0, 10, 0]
missionXMLGenerator.setObservationFromGrid()
missionXML = missionXMLGenerator.GenerateXML()
my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()
agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)
# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')



jumping = False
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        grid = observations.get(u'floor3x3', 0)
        frame = world_state.video_frames[0].pixels
        if world_state.number_of_rewards_since_last_state > 0:
            reward = taskAndRewards.taskDecoding(world_state.rewards[-1].getValue())
            for command in agentPolicy([grid, frame],reward):
                agent_host.sendCommand(command)

print()
print("Mission ended")
# Mission has ended.

