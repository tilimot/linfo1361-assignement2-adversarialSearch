import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import json
from datetime import datetime
import os
import glob


from agent import *
from mcts import *
from random import *
from game_manager import *
from random_agent import *
from mcts_improve import *

# Simulation parameters
#NUM_GAMES = 50  # Number of games per depth
#DEPTHS = [1, 2, 3, 4]  # Depths to test

   
def pipeline(params, n_exp, algorithm='MCTS'):
    folder_path = generate_folderpath()
    
    if algorithm == 'AlphaBeta':
        agent_class = Agent
        param_name = 'depth'
        opponent_class = AgentMcts
        opponent_params = {'iterations': 50}
    else:
        agent_class = AgentMcts2
        param_name = 'iterations'
        opponent_class = AgentMcts
        opponent_params = {'iterations': 50}

    # Run Experiments
    win_rate = run_experiment(agent_class, opponent_class, TextGameManager, 
                            folder_path, params, n_exp, param_name)
    print(win_rate)

    # Plot results
    stats = compute_move_time_stats(folder_path, param_name)
    
    if algorithm == 'AlphaBeta':
        plot_multi_depth(stats, folder_path)
        generate_ReflexionTime_Vs_RemainingPieces(folder_path, params[-1])
    else:
        plot_multi_iterations(stats, folder_path)
        
    generate_winrate_plot(folder_path, save=True)
   
def plot_multi_iterations(stats, folder_path=None):
    plt.figure(figsize=(10, 6))

    for iterations, data in sorted(stats.items()):
        move_indices = list(range(len(data["agent1"]["times"]["means"])))
        mean_times = data["agent1"]["times"]["means"]

        plt.plot(move_indices, mean_times, marker='o', linestyle='-', 
                label=f"{iterations} itérations")

    plt.xlabel("Move Index")
    plt.ylabel("Mean Move Time (seconds)")
    plt.title("Agent Move Time per Move for Different MCTS Iterations")
    plt.legend()
    plt.grid(True)
    
    if folder_path:
        plt.savefig(f"{folder_path}mcts_time_plot.png", dpi=300)
    plt.show()

def send_to_file(file_path,data):
    with open(file_path,'a') as f:
        f.write(data)

def generate_folderpath():
    folder_path = "stats/"
    os.makedirs(folder_path, exist_ok=True)
    return folder_path



def generate_filename():
    """Generates a filename based on the current date and time."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{timestamp}_game_stats"


def run_experiment(agent_class, opponent_class, game_manager_class, 
                  folder_path: str, params: list, num_games: int, param_name: str):
    
    results = defaultdict(lambda: {"wins": 0, "losses": 0})
    
    for param in params:
        print(f"Running {num_games} games for {param_name} {param}...")
        path = f"{folder_path}{generate_filename()}_{param_name}_{param}.json"
        
        for _ in range(num_games):
            agent_1 = agent_class(1, **{param_name: param})
            agent_2 = opponent_class(-1)
            game_manager = game_manager_class(agent_1, agent_2, display=False)
            
            p1_score, p2_score = game_manager.play()
            agent_1_time, agent_2_time = extract_timePerMove(game_manager)
            agent_1_pieces = game_manager.agent_1_piecesRemaining
            agent_2_pieces = game_manager.agent_2_piecesRemaining
            
            save_game_data(
                path,
                agent1={"times": agent_1_time, "pieces": agent_1_pieces},
                agent2={"times": agent_2_time, "pieces": agent_2_pieces},
                winner=p1_score,
                param_value=param,
                param_name=param_name
            )
            
            results[param]["wins"] += (1 if p1_score > 0 else 0)
            results[param]["losses"] += (1 if p1_score < 0 else 0)
    
    save_game_data(f"{folder_path}win_rate.json", win_rate=results)
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


def save_game_data(file_path, agent1=None, agent2=None, winner=None, param_value=None, param_name=None, win_rate=None):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    if win_rate is not None:
        data = win_rate
    else:
        data[timestamp] = {
            "agent1": agent1,
            "agent2": agent2,
            "winner": winner,
            param_name: param_value  # Utilisation dynamique du nom du paramètre
        }

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


    plt.plot(moves, agent_1_time, label="Agent 1", marker="o", linestyle="-", color="red")
    plt.plot(moves, agent_2_time, label="Agent 2", marker="s", linestyle="--", color="black")


    plt.xlabel("Numéro du coup")
    plt.ylabel("Temps de réflexion (s)")
    plt.title(f"Temps de réflexion par coup pour chaque agent. Profondeur AlphaBeta = {depth}")
    plt.legend()
    plt.grid(True)


    plt.show()

    date = generate_filename()
    plt.savefig(".\\graphs\\"+date+"_game_time_plot.png", dpi=300)




def compute_move_time_stats(directory, param_name='depth'):
    stats = {}
    
    for file_path in glob.glob(os.path.join(directory, "*.json")):
        if "game_stats" in file_path: 
            param = int(file_path.split('_')[-1].split('.')[0])
            
            with open(file_path, 'r') as f:
                data = json.load(f)

            agent1_moves = []
            agent2_moves = []
            agent1_pieces = []
            agent2_pieces = []
            
            max_moves = 0

            for game in data.values():
                agent1_times = game["agent1"]["times"]
                agent2_times = game["agent2"]["times"]
                a1_pieces = game["agent1"]["pieces"]
                a2_pieces = game["agent2"]["pieces"]
                
                max_moves = max(max_moves, len(agent1_times), len(agent2_times))
                
                agent1_moves.append(agent1_times)
                agent2_moves.append(agent2_times)
                agent1_pieces.append(a1_pieces)
                agent2_pieces.append(a2_pieces)


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

            stats[param] = {
                "agent1": {"times": {"means": agent1_means, "stds": agent1_stds}, "pieces": agent1_pieces},
                "agent2": {"times": {"means": agent2_means, "stds": agent2_stds}, "pieces": agent2_pieces}
            }
    
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



def plot_time_and_pieces(agent_data,  depth,agent_name="agent1",folder_path=None):
    times = agent_data[depth][agent_name]['times']['means']
    pieces = agent_data[depth][agent_name]["pieces"][0]

    # Sécuriser pour éviter mismatch
    min_len = min(len(times), len(pieces))
    times = times[:min_len]
    pieces = pieces[:min_len]
    turns = list(range(1, min_len + 1))

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color_time = 'tab:blue'
    ax1.set_xlabel('Numéro du coup')
    ax1.set_ylabel('Temps de réflexion (s)', color=color_time)
    ax1.plot(turns, times, label='Temps de réflexion', color=color_time)
    ax1.tick_params(axis='y', labelcolor=color_time)

    ax2 = ax1.twinx()  # Deuxième axe Y
    color_pieces = 'tab:red'
    ax2.set_ylabel('Nombre de pièces restantes', color=color_pieces)
    ax2.plot(turns, pieces, label='Pièces restantes', color=color_pieces)
    ax2.tick_params(axis='y', labelcolor=color_pieces)

    plt.title(f"{agent_name} – Temps de réflexion et pièces restantes par coup. Profondeur: {depth}")
    fig.tight_layout()
    plt.grid(True)
    if folder_path != None:
        plt.savefig(folder_path+f"reflexionTime_vs_remainingPieces_{depth}.png", dpi=300)
    
    plt.show()





def load_winrate_data(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def compute_percentages(data):
    """Calcule les pourcentages à partir des données brutes"""
    params = sorted(data.keys(), key=lambda x: int(x))
    wins, draws, losses = [], [], []

    for param in params:
        total = data[param]["wins"] + data[param]["losses"]  # On suppose pas de draws explicites
        win_pct = (data[param]["wins"] / total) * 100 if total > 0 else 0
        loss_pct = (data[param]["losses"] / total) * 100 if total > 0 else 0
        draw_pct = 0

        wins.append(win_pct)
        losses.append(loss_pct)
        draws.append(draw_pct)

    return params, wins, draws, losses

def plot_winrate(depths, win_pct, draw_pct, loss_pct, save_path=None):
    x = range(len(depths))
    plt.figure(figsize=(10, 6))
    
    plt.bar(x, win_pct, label='Wins', color='green')
    plt.bar(x, draw_pct, bottom=win_pct, label='Draws', color='gray')
    plt.bar(x, loss_pct, bottom=[w + d for w, d in zip(win_pct, draw_pct)],
            label='Losses', color='red')

    plt.xticks(x, depths)
    plt.xlabel('Search Depth')
    plt.ylabel('Percentage (%)')
    plt.title('Win/Draw/Loss Percentage by Depth')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def generate_winrate_plot(folderpath, filename="win_rate.json", save=False):
    json_path = os.path.join(folderpath, filename)
    data = load_winrate_data(json_path)
    depths, wins, draws, losses = compute_percentages(data)
    
    save_path = None
    if save:
        save_path = os.path.join(folderpath, "winrate_plot.svg")  # or .png
    plot_winrate(depths, wins, draws, losses, save_path)



def generate_ReflexionTime_Vs_RemainingPieces(folder_path,depth):
    folder_path = folder_path
    stats = compute_move_time_stats(folder_path)

    for i in range (1,depth+1):
        plot_time_and_pieces(stats,i,folder_path=folder_path)

