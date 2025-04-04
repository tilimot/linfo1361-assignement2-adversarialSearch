from visual_game_manager import *
from game_manager import *
from stats import *

#depths=[1,2,3]
#pipeline(depths,2)


folder_path = "stats\\2025-04-04_17-13-12\\"
stats = compute_move_time_stats(folder_path)
times = stats[2]['agent1']['times']['means']
pieces = stats[2]['agent1']['pieces'][0]


def plot_time_vs_pieces(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    agent1_times = []
    agent1_pieces = []
    agent2_times = []
    agent2_pieces = []

    # Extraire les données de chaque partie
    for game in data.values():
        a1 = game["agent1"]
        a2 = game["agent2"]

        # Ajout des temps et des pièces
        agent1_times.extend(a1["times"])
        agent1_pieces.extend(a1["pieces"][:len(a1["times"])])  # pour éviter mismatch
        agent2_times.extend(a2["times"])
        agent2_pieces.extend(a2["pieces"][:len(a2["times"])])

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(agent1_pieces, agent1_times, label="Agent 1", alpha=0.6, color='blue')
    plt.scatter(agent2_pieces, agent2_times, label="Agent 2", alpha=0.6, color='red')
    plt.xlabel("Nombre de pièces restantes")
    plt.ylabel("Temps de réflexion (s)")
    plt.title("Temps de réflexion en fonction des pièces restantes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



plot_time_vs_pieces(folder_path+"2025-04-04_17-13-14_game_stats_depth_3.json")

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