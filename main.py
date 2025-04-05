from visual_game_manager import *
from game_manager import *
from stats import *
from alpha_beta_iterative import *


#Code to launch pipeline

depths=[3,4]
pipeline(depths,50,AlphaBetaIterative,Agent)
#generate_winrate_plot(".\\stats\\2025-04-05_18-01-30\\",save=True)



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