from visual_game_manager import *
from game_manager import *
from stats import *

#agent = Agent()
red = Agent(1,depth=1)
black = RandomAgent(-1)
#vg = VisualGameManager(red_agent=red,black_agent=black)
#vg.play()

tgm = TextGameManager(agent_1=red,agent_2=black,display=False)
print(tgm.play())
agent_1_time = tgm.time_agent_1
agent_2_time = tgm.time_agent_2

agent_1_file = generate_filename()
agent_2_file = generate_filename()
stat_folder = ".\\stats\\"

with open(agent_1_file,'w') as f1:
    f1.write(agent_1_time)
    
with open(agent_2_file, 'w') as f2:
    f2.write(agent_2_time)