import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import json
from datetime import datetime
import os
import glob


from agent import *
from random import *
from game_manager import *
from random_agent import *

# Simulation parameters
#NUM_GAMES = 50  # Number of games per depth
#DEPTHS = [1, 2, 3, 4]  # Depths to test

def pipeline(depths, n_exp):
    folder_path = generate_folderpath()

    # Run Experiments & store it into ./stats/ folder
    win_rate = run_experiment(Agent,RandomAgent, TextGameManager, folder_path,depths, n_exp)
    print(win_rate)

    # Plot results
    stats = compute_move_time_stats(folder_path)
    plot_multi_depth(stats, folder_path)
   
   
def send_to_file(file_path,data):
    with open(file_path,'a') as f:
        f.write(data)

def generate_folderpath():
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = "stats\\"+date+"\\"
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def generate_filename():
    """Generates a filename based on the current date and time."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{timestamp}_game_stats"


def run_experiment(agent_class, random_agent_class, game_manager_class, folder_path:str, depths:list, num_games:int):
    
    results = defaultdict(lambda: {"wins": 0, "losses": 0})
    
    for depth in depths:
        print(f"Running {num_games} games for depth {depth}...")
        path = folder_path+generate_filename()+"_depth_"+str(depth)+".json"
        for _ in range(num_games):
            agent_1 = agent_class(1, depth)
            agent_2 = random_agent_class(-1)
            game_manager = game_manager_class(agent_1, agent_2, display=False)
            
            p1_score, p2_score = game_manager.play()
            agent_1_time, agent_2_time = extract_timePerMove(game_manager)
            agent_1_piecesRemaining, agent_2_piecesRemaining = game_manager.agent_1_piecesRemaining, game_manager.agent_2_piecesRemaining
            
            agent1 = {"times":agent_1_time, "pieces":agent_1_piecesRemaining}
            agent2 = {"times":agent_2_time, "pieces":agent_2_piecesRemaining}
            
            
            
            save_game_data(path, agent1, agent2, p1_score, depth)
            
            results[depth]["wins"] += (1 if p1_score > p2_score else 0)
            results[depth]["losses"] += (1 if p1_score < p2_score else 0)
    
    save_game_data(folder_path+"win_rate.json",win_rate=results)

    return results


def extract_timePerMove(tgm:TextGameManager):
    '''
    Take an array of remaining time. 
    Return an array of time per move
    '''
    # Extract the array of time move
    agent_1_remaining_time = tgm.time_agent_1
    agent_2_remaining_time = tgm.time_agent_2
    
    # Create duplicata to compare
    agent_1_comparison_time = [300]+agent_1_remaining_time[:-1]
    agent_2_comparison_time = [300]+agent_2_remaining_time[:-1]

    agent_1_time = []
    agent_2_time = []
    
    # Create a list with a time for each move (tgm list is remaining time, not time for each move)
    for i in range (len(agent_1_remaining_time)):
        agent_1_time.append(agent_1_comparison_time[i]-agent_1_remaining_time[i])
    for i in range(len(agent_2_remaining_time)):
        agent_2_time.append(agent_2_comparison_time[i]-agent_2_remaining_time[i])
        
    return agent_1_time, agent_2_time


def save_game_data(file_path, agent1=None, agent2=None, winner=None, depth=None, win_rate=None):
    # Charger l'ancien fichier s'il existe
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Générer une clé unique pour cette partie
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Ajouter les données
    if win_rate!=None:
        data = win_rate
        
    else:
        data[timestamp] = {
            "agent1": agent1,
            "agent2": agent2,
            "winner": winner,
            "depth": depth
        }

    # Sauvegarder le fichier JSON mis à jour
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
        

def plot_move_per_time_game(agent_1_time:list,agent_2_time:list,depth):
    
    max_moves = max(len(agent_1_time), len(agent_2_time))

    if len(agent_1_time) < max_moves:
        agent_1_time.append(agent_1_time[-1])  # Répète le dernier temps
    if len(agent_2_time) < max_moves:
        agent_2_time.append(agent_2_time[-1])

    moves = list(range(1, len(agent_1_time) + 1))
                
    plt.figure(figsize=(10, 5))

    # Tracer les temps de réflexion des agents
    plt.plot(moves, agent_1_time, label="Agent 1", marker="o", linestyle="-", color="red")
    plt.plot(moves, agent_2_time, label="Agent 2", marker="s", linestyle="--", color="black")

    # Ajouter des titres et légendes
    plt.xlabel("Numéro du coup")
    plt.ylabel("Temps de réflexion (s)")
    plt.title(f"Temps de réflexion par coup pour chaque agent. Profondeur AlphaBeta = {depth}")
    plt.legend()
    plt.grid(True)

    # Afficher le graphique
    plt.show()

    date = generate_filename()
    plt.savefig(".\\graphs\\"+date+"_game_time_plot.png", dpi=300)




def compute_move_time_stats(directory):
    stats = {}  # Store stats for each depth
    
    # Loop through all JSON files in the directory
    for file_path in glob.glob(os.path.join(directory, "*.json")):
        if "win_rate" not in file_path: 
            depth = int(file_path[-6])        
            with open(file_path, 'r') as f:
                data = json.load(f)

            agent1_moves = []
            agent2_moves = []
            
            agent1_pieces = []
            agent2_pieces=[]
            
            
            # Ensure lists are long enough
            max_moves = 0

            # Extract move times per game
            for game in data.values():
                agent1_times = game["agent1"]["times"]
                agent2_times = game["agent2"]["times"]
                
                a1_pieces = game["agent1"]["pieces"]
                a2_pieces = game["agent2"]["pieces"]
                
                
                max_moves = max(max_moves, len(agent1_times), len(agent2_times))
                
                # Append to per-move lists
                agent1_moves.append(agent1_times)
                agent2_moves.append(agent2_times)
                agent1_pieces.append(a1_pieces)
                agent2_pieces.append(a2_pieces)

            # Compute mean and std for each move index
            agent1_means = []
            agent1_stds = []
            agent2_means = []
            agent2_stds = []

            for i in range(max_moves):
                move_times_1 = [game[i] for game in agent1_moves if i < len(game)]
                move_times_2 = [game[i] for game in agent2_moves if i < len(game)]

                agent1_means.append(np.mean(move_times_1) if move_times_1 else 0)
                agent1_stds.append(np.std(move_times_1) if move_times_1 else 0)

                agent2_means.append(np.mean(move_times_2) if move_times_2 else 0)
                agent2_stds.append(np.std(move_times_2) if move_times_2 else 0)

            # Store stats
            stats[depth] = {
                "agent1":{"times": {"means": agent1_means, "stds": agent1_stds}, "pieces": agent1_pieces },
                "agent2": {"times": {"means": agent2_means, "stds": agent2_stds},"pieces": agent2_pieces}
            }
        else : 
            pass

    return stats


def plot_multi_depth(stats, folder_path=None):
    plt.figure(figsize=(10, 6))

    # Loop through each depth and plot the mean move time
    for depth, data in sorted(stats.items()):
        move_indices = list(range(len(data["agent1"]["times"]["means"])))
        mean_times = data["agent1"]["times"]["means"]  # Use Agent 1's times, or average both agents

        plt.plot(move_indices, mean_times, marker='o', linestyle='-', label=f"Depth {depth}")

    # Labels and title
    plt.xlabel("Move Index")
    plt.ylabel("Mean Move Time (seconds)")
    plt.title("Agent Move Time per Move for Different Depths")
    plt.legend()
    plt.grid(True)
    
    if folder_path != None:
        plt.savefig(folder_path+"game_time_plot.png", dpi=300)

    plt.show()



def plot_stats(stats):
    depths = sorted(stats.keys())  # Get sorted depth values

    agent1_means = [stats[d]["agent1"]["mean"] for d in depths]
    agent1_stds = [stats[d]["agent1"]["std"] for d in depths]
    
    agent2_means = [stats[d]["agent2"]["mean"] for d in depths]
    agent2_stds = [stats[d]["agent2"]["std"] for d in depths]

    plt.figure(figsize=(10, 6))

    # Plot with error bars
    plt.errorbar(depths, agent1_means, yerr=agent1_stds, fmt='-o', label="Agent 1", capsize=5)
    plt.errorbar(depths, agent2_means, yerr=agent2_stds, fmt='-s', label="Agent 2", capsize=5)

    # Labels and title
    plt.xlabel("Search Depth")
    plt.ylabel("Mean Move Time (seconds)")
    plt.title("Agent Move Time vs Depth (with Standard Deviation)")
    plt.legend()
    plt.grid(True)

    plt.show()

import matplotlib.pyplot as plt

def plot_move_time(stats, depth):
    if depth not in stats:
        print(f"No data available for depth {depth}")
        return

    move_indices = list(range(len(stats[depth]["agent1"]["means"])))

    # Extract data
    agent1_means = stats[depth]["agent1"]["means"]
    agent1_stds = stats[depth]["agent1"]["stds"]
    
    agent2_means = stats[depth]["agent2"]["means"]
    agent2_stds = stats[depth]["agent2"]["stds"]

    plt.figure(figsize=(10, 6))

    # Plot with error bars
    plt.errorbar(move_indices, agent1_means, yerr=agent1_stds, fmt='-o', label="Agent 1", capsize=5)
    plt.errorbar(move_indices, agent2_means, yerr=agent2_stds, fmt='-s', label="Agent 2", capsize=5)

    # Labels and title
    plt.xlabel("Move Index")
    plt.ylabel("Mean Move Time (seconds)")
    plt.title(f"Agent Move Time per Move (Depth {depth})")
    plt.legend()
    plt.grid(True)

    plt.show()

def plot_move_time_all_depth(stats, depth_max):
    if depth_max not in stats:
        print(f"No data available for depth {depth_max}")
        return
    for i in range(1,depth_max+1):
        move_indices = list(range(len(stats[i][f"agent{i}"]["means"])))

        # Extract data
        agent1_means = stats[i][f"agent{i}"]["means"]

        plt.figure(figsize=(10, 6))

        # Plot with error bars
        plt.errorbar(move_indices, agent1_means, fmt='-o', label="Agent 1", capsize=5)

    # Labels and title
    plt.xlabel("Move Index")
    plt.ylabel("Mean Move Time (seconds)")
    plt.title(f"Agent Move Time per Move (Depth)")
    plt.legend()
    plt.grid(True)

    plt.show()







    

#stats = compute_move_time_stats("stats")
#plot_multi_depth(stats)  # Change depth as needed



