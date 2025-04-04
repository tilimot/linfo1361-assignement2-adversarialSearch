from visual_game_manager import *
from game_manager import *
from stats import *


# Init
depths=[1,2,3,4]

date = datetime.now().strftime("%Y-%m-%d")
folder_path = "stats\\"+date+"\\"
os.makedirs(folder_path, exist_ok=True) #create folder


# Run Experiments
a = run_experiment(Agent,RandomAgent, TextGameManager, folder_path,depths, 100)

# Plot results
stats = compute_move_time_stats(folder_path)
plot_multi_depth(stats)  # Change depth as needed


''''
DEPTH = 2

#agent = Agent()
red = Agent(1,depth=DEPTH)
black = RandomAgent(-1)
#vg = VisualGameManager(red_agent=red,black_agent=black)
#vg.play()

tgm = TextGameManager(agent_1=red,agent_2=black,display=True)
print(tgm.play())

'''
