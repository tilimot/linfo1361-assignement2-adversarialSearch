from visual_game_manager import *
from game_manager import *
from stats import *
from mcts import AgentMcts

red = AgentMcts(1, iterations=1000)
black = RandomAgent(-1)
vg = VisualGameManager(red_agent=red,black_agent=black)
vg.play()

# tgm = TextGameManager(agent_1=red, agent_2=black, display=False)
# print(tgm.play())x    

# agent_1_time = tgm.time_agent_1  # C'est une liste
# agent_2_time = tgm.time_agent_2  # C'est une liste

# agent_1_file = generate_filename()
# agent_2_file = generate_filename()

# # Écriture des temps (convertir la liste en string)
# with open(agent_1_file, 'w') as f1:
#     f1.write('\n'.join(map(str, agent_1_time)))  # Convertit chaque élément en string et les joint par des retours à la ligne
    
# with open(agent_2_file, 'w') as f2:
#     f2.write('\n'.join(map(str, agent_2_time)))