from visual_game_manager import *
from game_manager import *
from stats import *


#Code to launch pipeline
depths=[1,2,3,4,5]
pipeline(depths,50)




'''
#Code to play 1 game visual or text

DEPTH = 2

#agent = Agent()
red = Agent(1,depth=DEPTH)
black = RandomAgent(-1)
vg = VisualGameManager(red_agent=red,black_agent=black)
vg.play()

#tgm = TextGameManager(agent_1=red,agent_2=black,display=True)
#print(tgm.play())

'''