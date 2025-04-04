from visual_game_manager import *
from game_manager import *
from stats import *

#depths=[1,2,3]
#pipeline(depths,2)


folder_path = "stats\\2025-04-04_17-13-12\\"
stats = compute_move_time_stats(folder_path)
print(stats)
times = stats[2]['agent1']['times']['means']
pieces = stats[2]['agent1']['pieces'][0]


plot_time_and_pieces(stats,3)
'''

DEPTH = 2

#agent = Agent()
red = Agent(1,depth=DEPTH)
black = RandomAgent(-1)
vg = VisualGameManager(red_agent=red,black_agent=black)
vg.play()

#tgm = TextGameManager(agent_1=red,agent_2=black,display=True)
#print(tgm.play())

'''