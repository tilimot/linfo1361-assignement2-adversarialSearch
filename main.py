from visual_game_manager import *
from game_manager import *
from stats import *

def pipeline(depths, n_exp):
    folder_path = generate_folderpath()

    # Run Experiments & store it into ./stats/ folder
    win_rate = run_experiment(Agent,RandomAgent, TextGameManager, folder_path,depths, n_exp)

    # Plot results
    stats = compute_move_time_stats(folder_path)
    plot_multi_depth(stats, folder_path)
    


depths=[1,2]
pipeline(depths,5)


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
