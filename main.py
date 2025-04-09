from visual_game_manager import *
from game_manager import *
from stats import *
from mcts import AgentMcts
from mcts_improve import AgentMcts2
from mcts_improve3 import *
#Code to launch pipeline
# depths=[1,2,3,4]
# pipeline(depths,50, algorithm='AlphaBeta')

# iterations = [50]
# pipeline(iterations, 25, algorithm='MCTS')

# agent1 = AgentMctsB(1, 50, 0.7)
# agent2 = AgentMcts(-1, 50)

# for i in range(10):
#     tgm = TextGameManager(agent_1=agent2,agent_2=agent1,display=False)
#     print(tgm.play())

# vg = VisualGameManager(red_agent=agent1,black_agent=agent2)
# vg.play()

import time
import matplotlib.pyplot as plt

agent1 = AgentMcts(1, 50)
agent2 = AgentMcts3(-1, 50)

num_games = 25
results = [] 
durations = []

for i in range(num_games):
    start_time = time.time()
    tgm = TextGameManager(agent_1=agent1, agent_2=agent2, display=False)
    result = tgm.play()
    end_time = time.time()

    results.append(result)
    durations.append(end_time - start_time)

    print(f"Game {i + 1}/{num_games}: Result = {result}, Duration = {end_time - start_time:.2f}s")

agent1_wins = sum(1 for r in results if r[0] == 1)
agent2_wins = sum(1 for r in results if r[1] == 1)
draws = sum(1 for r in results if r == (0, 0))

print("\n=== Résultats ===")
print(f"Agent 1 (AgentMcts) Wins: {agent1_wins}")
print(f"Agent 2 (AgentMcts3) Wins: {agent2_wins}")
print(f"Draws: {draws}")
print(f"Durée moyenne par partie: {sum(durations) / len(durations):.2f}s")

labels = ['AgentMcts3 Wins', 'AgentMcts Wins', 'Draws']
values = [agent1_wins, agent2_wins, draws]

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.bar(labels, values, color=['blue', 'red', 'gray'])
plt.title("Résultats des parties")
plt.ylabel("Nombre de victoires")
plt.xlabel("Résultat")

plt.subplot(1, 2, 2)
plt.plot(range(1, num_games + 1), durations, marker='o', color='green')
plt.title("Durée des parties")
plt.ylabel("Durée (secondes)")
plt.xlabel("Partie")

plt.tight_layout()
plt.show()

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